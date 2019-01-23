#!/usr/bin/env python

import re
import json
import sys
import fileinput

def label(s):
    m = re.search(r'\b[A-Z]+$', s)
    if not m: return
    return m.group(0)

def body(s):
    m = re.match(r'(.*)(?=\b[A-Z]+$)', s)
    if m: 
        out = m.group(1)
    else:
        out = s
    return out.strip().strip(',')

def parse(s):
    info = dict()
    chunks = s.split(':')
    for i in range(len(chunks) - 1):
        l = label(chunks[i])
        if not l: continue
        info[l] = body(chunks[i + 1])
    return info

builds = dict()

for line in fileinput.input():
    line = line.strip()
    with open(line) as f:
        builds[line] = parse(f.read())

json.dump(builds, sys.stdout, indent=2)
