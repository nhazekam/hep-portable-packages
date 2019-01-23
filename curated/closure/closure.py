#!/usr/bin/env python

import sys
import json
import random

SAMPLES = 100
PICKS = 1000

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

choice_sizes = [list() for i in range(PICKS)]
closure_sizes = [list() for i in range(PICKS)]
choice_counts = [list() for i in range(PICKS)]
closure_counts = [list() for i in range(PICKS)]

deps = json.load(sys.stdin)

for i in range(SAMPLES):
    choice = set()
    out = set() 
    sys.stderr.write('{} '.format(i))
    for j in range(PICKS):
        new_pkg = random.choice(deps.keys())
        choice.add(new_pkg)
        closure(deps, new_pkg, out)
        choice_counts[j].append(len(choice))
        closure_counts[j].append(len(out))
        choice_sizes[j].append(size(deps, choice))
        closure_sizes[j].append(size(deps, out))

print('picks choicecount closurecount choicesize closuresize')
for i in range(PICKS):
    print('{} {} {} {} {}'.format(
        i,
        smedian(choice_counts[i]),
        smedian(closure_counts[i]),
        smedian(choice_sizes[i]),
        smedian(closure_sizes[i]),
    ))

sys.stderr.write('\n')
