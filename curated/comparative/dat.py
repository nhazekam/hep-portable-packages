#!/usr/bin/env python

import sys
import json

INST = ['overhead', 'efficiency', 'images', 'imagesizes', 'pkgs',
        'realsize', 'reqsize', 'size', 'upkgs', 'usize']
CUM = ['byteswritten', 'deletes', 'inserts', 'merges', 'hits', 'hitrate',
       'peaksize', 'reqwritten']

def smedian(lst):
    lst.sort()
    return median(lst)


def median(lst):
    # lst must already be sorted!
    if len(lst) == 0: return 0
    if len(lst) == 1: return lst[0]
    i = len(lst) // 2
    if len(lst) % 2 == 0:
        return (lst[i] + lst[i - 1]) / 2
    else:
        return lst[i]

def sample_final(samples, field):
    return samples[-1][field]

def sample_median(samples, field):
    values = [s[field] for s in samples]
    values.sort()
    return median(values)


raw = json.load(sys.stdin)[sys.argv[1]]
dat = dict()

for alpha, runs in raw.items():
    dat[float(alpha)] = runs
    for stream in runs:
        p = 0
        rw = 0
        for sample in stream:
            sample['overhead'] = sample['realsize'] - sample['reqsize']
            sample['efficiency'] = float(sample['reqsize'])/sample['realsize']
            rw += sample['reqsize']
            sample['reqwritten'] = rw
            p = max(sample['size'], p)
            sample['peaksize'] = p
            sample['hitrate'] = float(sample['hits'])/(sample['hits']+sample['inserts']+sample['merges'])

print(' '.join(['alpha'] + INST + CUM))

alphas = dat.keys()
alphas.sort()

for i in alphas:
    cc = [str(smedian([sample_final(stream, f) for stream in dat[i]])) for f in CUM]
    ci = [str(smedian([sample_median(stream, f) for stream in dat[i]])) for f in INST]
    print(' '.join([str(i)] + ci + cc))
