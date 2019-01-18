#!/usr/bin/env python

import sys
import json

import sim


def extract(samples, field, step):
    values = [s[step][field] for s in samples]
    values.sort()
    return sim.median(values)

dat = json.load(sys.stdin)[sys.argv[1]][sys.argv[2]]

for run in dat:
    for sample in run:
        sample['efficiency'] = float(sample['reqsize']) / sample['realsize']

fields = dat[0][0].keys()
fields.sort()
print(' '.join(['step'] + fields))

for i in range(len(dat[0])):
    cols = [str(extract(dat, f, i)) for f in fields]
    print(' '.join([str(i)] + cols))
