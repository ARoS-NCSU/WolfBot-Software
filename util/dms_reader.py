#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot as wb
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', type=int, default=1)
parser.add_argument('-c', '--continuous', action='store_true', default=False)
args = parser.parse_args()

w = wb.wolfbot()

try:
    count = 0
    while count < args.num or args.continuous:
        dms = w.dms_mux.read_all()
        for name, val in sorted(dms.items()):
            print "name: {:3}, val: {:4d}".format(name, val)
        print
        time.sleep(0.1)
        count += 1
except KeyboardInterrupt:
    pass

