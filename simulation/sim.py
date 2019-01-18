#!/usr/bin/env python

import sys
import json
import random
import numbers
import itertools
import collections
import multiprocessing

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

def real_img(v):
    return isinstance(v, numbers.Integral)

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
    def __init__(self, deps, alpha):
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
        self.workers = {(): WORKERS}
        self.pool = {}

    def unique(self):
        return {item for subset in self.contents.keys() for item in subset}

    def total(self):
        return [item for (k, v) in self.contents.items() for item in k if real_img(v)]

    def pkgs(self):
        return len(self.total())

    def unique_pkgs(self):
        return len(self.unique())

    def unique_size(self):
        return sum([size(self.deps, [x]) for x in self.unique()])

    def requests(self):
        return self.contents.keys()

    def images(self):
        return [k for k, v in self.contents.items() if real_img(v)]

    def image_sizes(self):
        out = [v for k, v in self.contents.items() if real_img(v)]
        out.sort()
        return out

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
            "requests": len(self.requests()),
            "images": len(self.images()),
            "imagesizes": median(self.image_sizes()),
            "activeimgs": len(self.workers),
            "pool": len(self.pool),
            "hits": self.hits,
        }

    def push_workers(self, img, count):
        transfers = 0
        avail = self.workers.pop(img, 0)
        count -= avail
        while count > 0:
            other = random.choice(self.workers.keys())
            self.workers[other] -= 1
            count -= 1
            transfers += 1
            if self.workers[other] <= 0:
                self.workers.pop(other)
        self.workers[img] = avail + transfers
        return transfers

    def tidy(self, img=None):
        if img is None:
            for img in self.contents.keys():
                self.tidy(img)
            return
        if not img in self.contents: return False
        if real_img(self.contents[img]): return True
        live = self.tidy(self.contents[img])
        if not live: self.contents.pop(img)
        return live

    def merge(self, existing, img):
        self.size -= self.contents.pop(existing)
        new_img = existing | img
        self.contents[existing] = new_img
        self.contents[img] = new_img
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

    def hit(self, img):
        # for LRU
        tmp = self.contents.pop(img)
        self.contents[img] = tmp
        if real_img(tmp):
            req_size = tmp
            real_size = tmp
        else:
            req_size = size(self.deps, img)
            img = self.find_parent(img)
            tmp = self.contents.pop(img)
            self.contents[img] = tmp
            real_size = tmp

        self.hits += 1
        return req_size, real_size, img

    def decide(self, img):
        best_img = None
        best_dst = 2.0

        if img in self.contents:
            return self.hit(img)

        for a in self.contents.keys():
            if not real_img(self.contents[a]):
                continue
            j = jaccard(img, a)
            if j <= self.alpha:
                if j < best_dst:
                    best_dst = j
                    best_img = a

        if best_img is not None:
            return self.merge(best_img, img)

        return self.insert(img)

    def eat(self, img):
        req_size, real_size, new_img = self.decide(img)
        self.log.append(self.stats())
        self.log[-1]["reqsize"] = req_size
        self.log[-1]["realsize"] = real_size
        self.log[-1]["workers"] = random.randrange(1, WORKERS)
        self.log[-1]["tx"] = self.push_workers(new_img, self.log[-1]["workers"])

    def find_parent(self, img):
        if real_img(self.contents[img]):
            return img
        return self.find_parent(self.contents[img])

    def shrink(self):
        dead_img = None
        dead_size = None
        while self.size > CAPACITY:
            if dead_img is None or dead_size is None:
                (dead_img, dead_size) = self.contents.popitem(False)
            if not real_img(dead_size):
                dead_img = dead_size
                dead_size = self.contents.pop(dead_img, None)
                continue
            #print('pop {} of {}'.format(id(dead_img), len(dead_img)))
            self.deletes += 1
            self.size -= dead_size
            dead_img = None

    def run_from_pool(self):
        img = random.choice(self.pool.keys())
        self.pool[img] -= 1
        if self.pool[img] < 0:
            self.pool.pop(img)
        self.eat(img)
        self.shrink()
        self.tidy()

    def process(self, stream):
        for img in stream:
            while len(self.pool) > 0:
                if REUSE > 0 and random.random() < 1.0/(REUSE+2): break
                self.run_from_pool()
            self.pool[img] = REUSE
        while len(self.pool) > 0:
            self.run_from_pool()
        return self.log

def run(params):
    alpha, deps = params
    out = {}
    for i in range(3):
        c = Cache(deps, alpha)
        d = Cache(deps, alpha)
        c.process(itertools.islice(Stream(deps), JOBS))
        d.process(itertools.islice(BlindStream(deps), JOBS))
        out['tree'] = c.log
        out['blind'] = d.log
    sys.stderr.write('{} '.format(alpha))
    return out
    

if __name__ == '__main__':
    deps = json.load(sys.stdin)
    for d in deps.values():
        d['size'].sort()

    out = {
        "tree": {},
        "blind": {},
    }

    alphas = [x / 100.0 for x in range(40, 101)]

    for alpha in alphas:
        out['tree'][alpha] = []
        out['blind'][alpha] = []

    p = multiprocessing.Pool(61)
    results = p.map(run, [(i, deps) for i in alphas])
    print('')

    for i in range(len(alphas)):
        out['tree'][alphas[i]].append(results[i]['tree'])
        out['blind'][alphas[i]].append(results[i]['blind'])

    json.dump(out, sys.stdout, indent=2)

    #c = Cache(deps, 1e12, 0.6)
    #c.eat(Stream(deps, 100))
