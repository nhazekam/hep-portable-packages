#!/usr/bin/env python

import sys
import json

import sim

INST = ['overhead', 'efficiency', 'images', 'imagesizes', 'pkgs',
        'realsize', 'reqsize', 'size', 'upkgs', 'usize',
        'txcost', 'pool', 'activeimgs', 'workers', 'tx']
CUM = ['byteswritten', 'deletes', 'inserts', 'merges', 'hits']

def sample_final(samples, field):
    return samples[-1][field]

def sample_median(samples, field):
    values = [s[field] for s in samples]
    values.sort()
    return sim.median(values)

raw = json.load(sys.stdin)[sys.argv[1]]
dat = dict()

for alpha, runs in raw.items():
    dat[float(alpha)] = runs
    for stream in runs:
        for sample in stream:
            sample['overhead'] = sample['realsize'] - sample['reqsize']
            sample['efficiency'] = float(sample['reqsize'])/sample['realsize']
            sample['txcost'] = sample['tx'] * sample['realsize']

print(' '.join(['alpha'] + INST + CUM))

alphas = dat.keys()
alphas.sort()

for i in alphas:
    cc = [str(sim.smedian([sample_final(stream, f) for stream in dat[i]])) for f in CUM]
    ci = [str(sim.smedian([sample_median(stream, f) for stream in dat[i]])) for f in INST]
    print(' '.join([str(i)] + ci + cc))
