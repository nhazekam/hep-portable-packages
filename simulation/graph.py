#!/usr/bin/env python

import sys
import json

def closure(graph, deps, pkg):
    if pkg in graph: return
    graph[pkg] = deps[pkg]
    for p in deps[pkg]['deps']:
        closure(graph, deps, p)

with open(sys.argv[1]) as f:
    deps = json.load(f)
with open(sys.argv[2]) as f:
    recent = json.load(f)

graph = dict()

for p, (v, h) in recent.items():
    pkg = '{}-{}-{}'.format(p, v, h)
    closure(graph, deps, pkg)

print('digraph {')

for k, v in graph.items():
    #print('"{}";'.format(k))

    for d in v['deps']:
        print('"{}" -> "{}";'.format(k, d))

print('}')
