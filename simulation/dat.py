#!/usr/bin/env python

import sys
import json

import sim

INST = ['overhead', 'efficiency', 'images', 'imagesizes', 'pkgs',
        'realsize', 'reqsize', 'size', 'upkgs', 'usize',
        'pool', 'activeimgs', 'workers']
CUM = ['byteswritten', 'deletes', 'inserts', 'merges', 'hits',
       'tx', 'txcost', 'peaksize', 'cost']

def sample_final(samples, field):
    return samples[-1][field]

def sample_median(samples, field):
    values = [s[field] for s in samples]
    values.sort()
    return sim.median(values)

def cost2(samples):
    return sample_median(samples,'size') / sample_median(samples, 'usize') * sample_final(samples,'peaksize') + sample_final(samples, 'txcost')/1000

raw = json.load(sys.stdin)[sys.argv[1]]
dat = dict()

for alpha, runs in raw.items():
    dat[float(alpha)] = runs
    for stream in runs:
        p = 0
        for sample in stream:
            sample['overhead'] = sample['realsize'] - sample['reqsize']
            sample['efficiency'] = float(sample['reqsize'])/sample['realsize']
            p = max(sample['size'], p)
            sample['peaksize'] = p
            sample['cost'] = sample['peaksize'] + sample['txcost']/1000

print(' '.join(['alpha', 'cost2'] + INST + CUM))

alphas = dat.keys()
alphas.sort()

for i in alphas:
    other = str(sim.smedian([cost2(stream) for stream in dat[i]]))
    cc = [str(sim.smedian([sample_final(stream, f) for stream in dat[i]])) for f in CUM]
    ci = [str(sim.smedian([sample_median(stream, f) for stream in dat[i]])) for f in INST]
    print(' '.join([str(i), other] + ci + cc))
