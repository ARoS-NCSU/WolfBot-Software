#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot
from math import degrees, radians, sin, cos, atan2, sqrt
import time
import signal
import os

def cleanup(signum, frame):
    wb.stop()
    os._exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

wb = wolfbot.wolfbot()

vel_x = 0
vel_y = 0
while True:
    dms = wb.dms_mux.read_all()
    x_tot = 0.0
    y_tot = 0.0
    for name, val in sorted(dms.items()):
        angle = name
        #print "name: ", name, "angle: ", angle, "val: ", val
        if val < 200:
            continue
        if val > 1700:
            val = 1700
        x = val * cos(radians(angle))
        y = val * sin(radians(angle))
        x_tot += x
        y_tot += y

    decay = 0.7
    vel_x = (decay * vel_x) - x_tot
    vel_y = (decay * vel_y) - y_tot
    vel_mag = 100 * sqrt((vel_x)**2 + vel_y**2)/3400  # normalize to ??
    vel_mag = min(100, vel_mag)
    vel_ang = degrees(atan2(vel_y, vel_x)) % 360

    if vel_mag > 50:
        wb.move(vel_ang, vel_mag)
    else:
        wb.stop()

    time.sleep(0.01)

