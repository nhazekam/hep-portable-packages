#!/usr/bin/env python

import re
import json
import sys
import fileinput

def package(s):
    path_pieces = s.split('/')
    if len(path_pieces) >= 4: 
        out = path_pieces[3]
        if len(path_pieces) >= 5:
            out += '-'
            out += path_pieces[4]
    else:
        out = s
    return out

def parse(f):
    info = dict()
    s = f.readline()
    while s:
        chunks = s.split(":")
	if len(chunks) < 2:
            s = f.readline()
            continue
        pack = chunks[1].split(' ')
	if len(pack) < 2:
            s = f.readline()
            continue
        p = package(pack[0])
        if p:
            info[p] = info.get(p, 0) + 1
            packages[p] = packages.get(p, 0) + 1
        s = f.readline()
    return info

builds = dict()
packages = dict()

for line in fileinput.input():
    line = line.strip()
    with open(line) as f:
        builds[line] = parse(f)

json.dump(packages, sys.stdout, indent=2)

