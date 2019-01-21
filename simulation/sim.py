#!/usr/bin/env python

import sys
import json
import random
import numbers
import itertools
import collections
import multiprocessing
import argparse

from numpy.random import choice

CAPACITY = 1.5e12
MAXREQ = 100

def median(lst):
    # lst must already be sorted!
    if len(lst) == 0: return 0
    if len(lst) == 1: return lst[0]
    i = len(lst) // 2
    if len(lst) % 2 == 0:
        return (lst[i] + lst[i - 1]) / 2
    else:
        return lst[i]

def smedian(lst):
    lst.sort()
    return median(lst)

def jaccard(a, b):
    return 1 - float(len(a & b))/len(a | b)

def size(deps, img):
    accum = 0
    for pkg in img:
        accum += median(deps[pkg]['size'])
    return accum

def closure(deps, pkg, res):
    if pkg in res: return
    res.add(pkg)
    for p in deps[pkg]['deps']:
        closure(deps, p, res)

def blind(deps, img):
    return set(random.sample(deps.keys(), len(img)))

class DistStream:
    def __init__(self, deps, deps_freq):
        self.deps = deps
        self.dep_freq = deps_freq
    def __iter__(self):
        return self
    def next(self):
        out = set()
        count = random.randrange(1, MAXREQ)
        for pkg in choice(self.deps.keys(), count, False, self.dep_freq):
           closure(deps, pkg, out) 
        return frozenset(out)


class Stream:
    def __init__(self, deps):
        self.deps = deps
    def __iter__(self):
        return self
    def next(self):
        out = set()
        count = random.randrange(1, MAXREQ)
        for pkg in random.sample(self.deps.keys(), count):
           closure(deps, pkg, out) 
        return frozenset(out)

class BlindStream:
    def __init__(self, deps):
        self.deps = deps
        self.stream = Stream(deps)
    def __iter__(self):
        return self
    def next(self):
        return frozenset(blind(self.deps, self.stream.next()))

class Cache:
    def __init__(self, deps, alpha, reuse):
        self.reuse = reuse
        self.deps = deps
        self.size = 0
        self.alpha = alpha
        self.bytes_written = 0
        self.merges = 0
        self.inserts = 0
        self.deletes = 0
        self.hits = 0
        self.contents = collections.OrderedDict()
        self.log = []
        self.distances = {}
        self.subsets = {}

    def jaccard(self, a, b):
        if (a, b) in self.distances:
            return self.distances[(a, b)]
        out = jaccard(a, b)
        self.distances[(a, b)] = out
        self.distances[(b, a)] = out
        return out

    def issubset(self, a, b):
        if (a, b) in self.subsets:
            return self.subsets[(a, b)]
        out = a.issubset(b)
        self.subsets[(a, b)] = out
        return out

    def unique(self):
        return {item for subset in self.contents.keys() for item in subset}

    def total(self):
        return [item for subset in self.contents.keys() for item in subset]

    def pkgs(self):
        return len(self.total())

    def unique_pkgs(self):
        return len(self.unique())

    def unique_size(self):
        return size(self.deps, self.unique())

    def images(self):
        return self.contents.keys()

    def image_sizes(self):
        return self.contents.values()

    def stats(self):
        return {
            "byteswritten": self.bytes_written,
            "pkgs": self.pkgs(),
            "upkgs": self.unique_pkgs(),
            "size": self.size,
            "merges": self.merges,
            "inserts": self.inserts,
            "deletes": self.deletes,
            "usize": self.unique_size(),
            "images": len(self.images()),
            "imagesizes": smedian(self.image_sizes()),
            "hits": self.hits,
        }

    def merge(self, existing, img):
        self.size -= self.contents.pop(existing)
        new_img = existing | img
        self.contents[new_img] = size(self.deps, new_img)
        self.size += self.contents[new_img]
        self.bytes_written += self.contents[new_img]
        self.merges += 1
        return size(self.deps, img), self.contents[new_img], new_img

    def insert(self, img):
        self.contents[img] = size(self.deps, img)
        self.size += self.contents[img]
        self.bytes_written += self.contents[img]
        self.inserts += 1
        return self.contents[img], self.contents[img], img

    def hit(self, real, img):
        # LRU touch
        tmp = self.contents.pop(real)
        self.contents[real] = tmp

        if real == img:
            req_size = tmp
        else:
            req_size = size(self.deps, img)

        self.hits += 1
        return req_size, tmp, real

    def decide(self, img):
        if img in self.contents:
            return self.hit(img, img)

        candidates = [(self.jaccard(img, x), x) for x in self.contents.keys()]
        candidates = [x for x in candidates if x[0] < self.alpha]
        candidates.sort(key=lambda x: x[0])

        for a in candidates:
            if self.issubset(img, a[1]):
                return self.hit(a[1], img)

        if len(candidates) > 0:
            return self.merge(candidates[0][1], img)

        return self.insert(img)

    def eat(self, img):
        req_size, real_size, new_img = self.decide(img)
        self.log.append(self.stats())
        self.log[-1]["reqsize"] = req_size
        self.log[-1]["realsize"] = real_size

    def shrink(self):
        dead_img = None
        dead_size = None
        while self.size > CAPACITY:
            dead_img, dead_size = self.contents.popitem(False)
            self.deletes += 1
            self.size -= dead_size

    def process(self, stream):
        pool = []
        for img in stream:
            for i in range(self.reuse):
                pool.append(img)
        random.shuffle(pool)
        for img in pool:
            self.eat(img)
            self.shrink()
        return self.log

def run(params):
    alpha, deps, deps_freq, reuse, jobs = params
    out = {}
    for i in range(10):
        b = Cache(deps, alpha, reuse)
        c = Cache(deps, alpha, reuse)
        d = Cache(deps, alpha, reuse)
        b.process(itertools.islice(DistStream(deps, deps_freq), jobs))
        c.process(itertools.islice(Stream(deps), jobs))
        d.process(itertools.islice(BlindStream(deps), jobs))
        out['dist'] = b.log
        out['tree'] = c.log
        out['blind'] = d.log
    sys.stderr.write('{} '.format(alpha))
    return out
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reuse', type=int)
    parser.add_argument('--jobs', type=int)
    args = parser.parse_args()

    deps = json.load(sys.stdin)
    for d in deps.values():
        d['size'].sort()

    deps_freq = []
    total = 0.0
    usage = open("sft.usage.json", 'r')
    freq = json.load(usage)
    for d in deps.keys():
        total += freq.get(d, 1.0)
        deps_freq.append(freq.get(d, 1))

    deps_freq[:] = [x / total for x in deps_freq]

    out = {
        "tree": {},
        "blind": {},
        "dist": {},
    }

    alphas = [x / 100.0 for x in range(40, 101)]

    for alpha in alphas:
        out['tree'][alpha] = []
        out['blind'][alpha] = []
        out['dist'][alpha] = []

    p = multiprocessing.Pool()
    results = p.map(run, [(i, deps, deps_freq, args.reuse, args.jobs) for i in alphas])
    #results = map(run, [(i, deps, deps_freq) for i in alphas])
    sys.stderr.write('\n')
    sys.stderr.flush()

    for i in range(len(alphas)):
        out['tree'][alphas[i]].append(results[i]['tree'])
        out['blind'][alphas[i]].append(results[i]['blind'])
        out['dist'][alphas[i]].append(results[i]['dist'])

    json.dump(out, sys.stdout, indent=2)
