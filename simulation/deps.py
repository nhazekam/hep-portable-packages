#!/usr/bin/env python

import fileinput
import json
import sys
import re

with open(sys.argv[1]) as f:
    builds = json.load(f)

sizes = dict()
with open(sys.argv[2]) as f:
    for line in f.readlines():
        (s, p) = line.split('\t')
        sizes[p.strip()] = int(s)

deps = dict()
for p, b in builds.items():
    pkg = '{}-{}-{}'.format(b["NAME"], b["VERSION"], b["HASH"])
    if not pkg in deps:
        deps[pkg] = {"size": list(), "deps": set()}
    deps[pkg]["size"].append(sizes[re.sub(r'[^/]*$', '', p)])
    if "DEPENDS" in b:
        deps[pkg]["deps"].update(b["DEPENDS"].split(","))

for e in deps.values():
    e["deps"] = [x for x in e["deps"] if x in deps]

json.dump(deps, sys.stdout, indent=2)
