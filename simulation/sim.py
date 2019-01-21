#!/usr/bin/env python

import sys
import json
import random
import numbers
import itertools
import collections
import multiprocessing

from numpy.random import choice

CAPACITY = 1e12
WORKERS = 1000
MAXREQ = 100
REUSE = 9
JOBS = 100

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

class Stream:
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

class BlindStream:
    def __init__(self, deps, deps_freq):
        self.deps = deps
        self.stream = Stream(deps, deps_freq)
    def __iter__(self):
        return self
    def next(self):
        return frozenset(blind(self.deps, self.stream.next()))

class Cache:
    def __init__(self, deps, alpha):
        self.deps = deps
        self.size = 0
        self.alpha = alpha
        self.bytes_written = 0
        self.merges = 0
        self.inserts = 0
        self.deletes = 0
        self.hits = 0
        self.tx = 0
        self.tx_cost = 0
        self.contents = collections.OrderedDict()
        self.log = []
        self.workers = collections.OrderedDict()
        self.workers[()] = WORKERS
        self.pool = {}
        self.distances = {}

    def lazy_jaccard(self, a, b):
        if (a, b) in self.distances:
            return self.distances[(a, b)]
        out = jaccard(a, b)
        self.distances[(a, b)] = out
        self.distances[(b, a)] = out
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
            "activeimgs": len(self.workers),
            "pool": len(self.pool),
            "hits": self.hits,
            "tx": self.tx,
            "txcost": self.tx_cost,
        }

    def push_workers(self, img, count):
        transfers = 0
        avail = self.workers.pop(img, 0)
        count -= avail
        while count > 0:
            other = self.workers.keys()[0]
            tx = min(count, self.workers[other])
            self.workers[other] -= tx
            count -= tx
            transfers += tx
            if self.workers[other] <= 0:
                self.workers.pop(other)
        self.workers[img] = avail + transfers
        return transfers

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

        # for worker simulation
        # prioritize stuff already on workers
        pushed = [(self.lazy_jaccard(img, x), x) for x in self.workers.keys() if x in self.contents]
        pushed = [x for x in pushed if x[0] < self.alpha]
        pushed.sort(key=lambda x: x[0])

        for a in pushed:
            if img.issubset(a[1]):
                return self.hit(a[1], img)

        candidates = [(self.lazy_jaccard(img, x), x) for x in self.contents.keys()]
        candidates = [x for x in candidates if x[0] < self.alpha]
        candidates.sort(key=lambda x: x[0])

        for a in candidates:
            if img.issubset(a[1]):
                return self.hit(a[1], img)

        if len(candidates) > 0:
            return self.merge(candidates[0][1], img)

        return self.insert(img)

    def eat(self, img):
        req_size, real_size, new_img = self.decide(img)
        self.log.append(self.stats())
        self.log[-1]["reqsize"] = req_size
        self.log[-1]["realsize"] = real_size
        self.log[-1]["workers"] = random.randrange(1, WORKERS//4)
        transfers = self.push_workers(new_img, self.log[-1]["workers"])
        self.tx += transfers
        self.tx_cost += transfers * real_size

    def shrink(self):
        dead_img = None
        dead_size = None
        while self.size > CAPACITY:
            dead_img, dead_size = self.contents.popitem(False)
            self.deletes += 1
            self.size -= dead_size

    def run_from_pool(self):
        img = random.choice(self.pool.keys())
        self.pool[img] -= 1
        if self.pool[img] < 0:
            self.pool.pop(img)
        self.eat(img)
        self.shrink()

    def process(self, stream):
        for img in stream:
            while len(self.pool) > 0:
                if REUSE > 0 and random.random() < 1.0/(2*REUSE): break
                self.run_from_pool()
            self.pool[img] = REUSE
        while len(self.pool) > 0:
            self.run_from_pool()
        return self.log

def run(params):
    alpha, deps, deps_freq = params
    out = {}
    for i in range(10):
        c = Cache(deps, alpha)
        d = Cache(deps, alpha)
        c.process(itertools.islice(Stream(deps, deps_freq), JOBS))
        d.process(itertools.islice(BlindStream(deps, deps_freq), JOBS))
        out['tree'] = c.log
        out['blind'] = d.log
    sys.stderr.write('{} '.format(alpha))
    return out
    

if __name__ == '__main__':
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
    }

    alphas = [x / 100.0 for x in range(40, 101)]

    for alpha in alphas:
        out['tree'][alpha] = []
        out['blind'][alpha] = []

    p = multiprocessing.Pool()
    results = p.map(run, [(i, deps, deps_freq) for i in alphas])
    #results = map(run, [(i, deps, deps_freq) for i in alphas])
    sys.stderr.write('\n')
    sys.stderr.flush()

    for i in range(len(alphas)):
        out['tree'][alphas[i]].append(results[i]['tree'])
        out['blind'][alphas[i]].append(results[i]['blind'])

    json.dump(out, sys.stdout, indent=2)
