#!/usr/bin/env python

import sys
import json
import random

import sim

SAMPLES = 100
PICKS = 1000

sizes = [list() for i in range(PICKS)]
counts = [list() for i in range(PICKS)]

deps = json.load(sys.stdin)

for i in range(SAMPLES):
    out = set() 
    sys.stderr.write('{} '.format(i))
    for j in range(PICKS):
        sim.closure(deps, random.choice(deps.keys()), out)
        counts[j].append(len(out))
        sizes[j].append(sim.size(deps, out))

for i in range(PICKS):
    sizes[i].sort()
    counts[i].sort()
    print('{} {} {}'.format(i, sim.median(counts[i]), sim.median(sizes[i])))
