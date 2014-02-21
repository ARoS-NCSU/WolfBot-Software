#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot as wb
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', type=int, default=1)
parser.add_argument('-c', '--continuous', action='store_true', default=False)
parser.add_argument('-i', '--inches', action='store_true', default=False)
args = parser.parse_args()

w = wb.wolfbot()

try:
    count = 0
    while count < args.num or args.continuous:
        if args.inches:
            dms = w.dms_mux.read_all(mode='inch')
            fmt_str = "name: {:3}, val: {:5.2f}"
        else:
            dms = w.dms_mux.read_all()
            fmt_str = "name: {:3}, val: {:3}"
        for name, val in sorted(dms.items()):
            print fmt_str.format(name, val)
        print
        time.sleep(0.05)
        count += 1
except KeyboardInterrupt:
    pass

