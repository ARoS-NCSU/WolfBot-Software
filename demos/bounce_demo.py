#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot as wb
from math import degrees, radians, sin, cos, atan2
import time

w = wb.wolfbot()

def shy(angle, mag):
    away = (angle + 180) % 360
    if mag < 50:
        w.stop()
    else:
        if mag > 100:
            mag = 100
        w.move(away, mag)

def bounce(angle, mag):
    if not hasattr(bounce, "speed"):
        bounce.speed = 0  # it doesn't exist yet, so initialize it
    speed = bounce.speed
    if mag > 50:
        speed = mag
    else:
        #away_speed -= 0.1
        pass
    w.move(away, speed)

away_speed = 0
while True:
    dms = w.dms_mux.read_all()
    x_tot = 0.0
    y_tot = 0.0
    for name, val in sorted(dms.items()):
        angle = name
        #print "name: ", name, "angle: ", angle, "val: ", val

        if val > 2000:
            val = 2000
        x = val * cos(radians(angle))
        y = val * sin(radians(angle))
        x_tot += x
        y_tot += y

    mag = 100 * (abs(x_tot) + abs(y_tot))/1000  # normalize to ??
    angle = degrees(atan2(y_tot, x_tot)) % 360
    #print "x_tot, y_tot:", x_tot, y_tot
    #print "mag, angle (sensed): ", mag, angle
    #print "angle (away): ", away
   
    shy(angle, mag)

    time.sleep(0.01)

