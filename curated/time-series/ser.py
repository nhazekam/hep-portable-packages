#!/usr/bin/env python

import sys
import json

def extract(samples, field, step):
    values = [s[step][field] for s in samples]
    values.sort()
    return sim.median(values)

dat = json.load(sys.stdin)[sys.argv[1]][sys.argv[2]][int(sys.argv[3])]

headers = dat[0].keys()
headers.sort()
print(' '.join(['step'] + headers))

for i in range(len(dat)):
    cols = [str(dat[i][c]) for c in headers]
    print(' '.join([str(i)] + cols))
