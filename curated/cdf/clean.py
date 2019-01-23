#!/usr/bin/env python
import fileinput

for a in fileinput.input():
    log, count = a.split()
    log = int(log)
    count = int(count)
    print("{} {}".format(2**log, count/1e6))
