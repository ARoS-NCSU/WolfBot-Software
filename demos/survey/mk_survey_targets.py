#!/usr/bin/python

"""
Make a list of survey targets
"""

import argparse

def zig_zag(start, end, steps):
    targets = []
    zs = linspace(start, end, steps)
    sign = 1 
    for z in zs:
        targets += [ (z,x*sign) for x in linspace(start, end, steps) ]
        sign *= -1
    return targets

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', type=int, default=11)

args = parser.parse_args()

from numpy import linspace
targets = zig_zag(-1,1,args.num)

for t in targets:
    print "{} {}".format(*t)

