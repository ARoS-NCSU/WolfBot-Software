#!/usr/bin/python

"""
Benchmark optitrack library
"""

import sys
import time

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import optitrack

opti = optitrack.Optitrack()

n = 100
print "Reading Optitrack pose %d times",
t0 = time.time()
for i in range(n):
    opti.get_pose()
elapsed = time.time() - t0
each = elapsed / n
rate = 1/each
print "Took %0.2f seconds (%0.2f ms/ea, %0.2f Hz)" % (elapsed, each*1000, rate)
