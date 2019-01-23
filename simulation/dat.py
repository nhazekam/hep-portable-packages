#!/usr/bin/env python

import sys
import json

import sim

INST = ['overhead', 'container_efficiency', 'cache_efficiency', 'images', 'imagesizes', 'pkgs',
        'realsize', 'reqsize', 'size', 'upkgs', 'usize']
CUM = ['byteswritten', 'deletes', 'inserts', 'merges', 'hits', 'hitrate',
       'peaksize', 'reqwritten']

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
        p = 0
        rw = 0
        for sample in stream:
            sample['overhead'] = sample['realsize'] - sample['reqsize']
            sample['container_efficiency'] = float(sample['reqsize'])/sample['realsize']
            sample['cache_efficiency'] = float(sample['usize'])/sample['size']
            p = max(sample['size'], p)
            sample['peaksize'] = p
            rw += sample['reqsize']
            sample['reqwritten'] = rw
            sample['hitrate'] = float(sample['hits'])/(sample['hits']+sample['inserts']+sample['merges'])

print(' '.join(['alpha'] + INST + CUM))

alphas = dat.keys()
alphas.sort()

for i in alphas:
    cc = [str(sim.smedian([sample_final(stream, f) for stream in dat[i]])) for f in CUM]
    ci = [str(sim.smedian([sample_median(stream, f) for stream in dat[i]])) for f in INST]
    print(' '.join([str(i)] + ci + cc))
