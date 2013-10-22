#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot as wb
import time

w = wb.wolfbot()

while True:
    dms = w.dms_mux.read_all()
    for name, val in sorted(dms.items()):
        angle = 360 - name
        print "name: ", name, "angle: ", angle, "val: ", val
    print
    time.sleep(0.1)

