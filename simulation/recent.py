#!/usr/bin/env python

from distutils.version import LooseVersion, StrictVersion
import json
import sys

builds = json.load(sys.stdin)

packages = dict()
recent = dict()

for b in builds.values():
    if ',' in b['VERSION']: continue
    if not b['NAME'] in packages:
        packages[b['NAME']] = dict()
    packages[b['NAME']][b['VERSION']] = b['HASH']

for pkg,vers in packages.items():
    for v, h in vers.items():
        if pkg in recent:
            if LooseVersion(v) > LooseVersion(recent[pkg][0]):
                recent[pkg] = (v, h)
        else:
            recent[pkg] = (v, h)

json.dump(recent, sys.stdout, indent=2)
