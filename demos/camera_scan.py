#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot as wb
import time

w = wb.wolfbot()

def slow_tilt(angle, rate, delay = 0.05):
    while abs(w.camera.tilt - angle) > 1:
        if w.camera.tilt < angle:
            w.camera.set_tilt(w.camera.tilt + rate)
        else:
            w.camera.set_tilt(w.camera.tilt - rate)
        time.sleep(delay)

w.camera.set_tilt(135)
    
w.move(90,70)
time.sleep(2.5)
w.stop()
time.sleep(0.2)

w.move(-90,70)
time.sleep(5.0)
w.stop()
time.sleep(0.2)

w.move(90,70)
time.sleep(2.5)
w.stop()

time.sleep(1.0)

##########
slow_tilt(95, 2)
time.sleep(0.5)
slow_tilt(170, 2)
time.sleep(0.5)
slow_tilt(95, 2)
time.sleep(0.5)
slow_tilt(170, 2)
time.sleep(0.5)
slow_tilt(95, 2)
time.sleep(0.5)
slow_tilt(150, 2)
time.sleep(0.5)

#################
turn_rate = 25
w.turn('cw', turn_rate)
time.sleep(1)
w.stop()

w.turn('ccw', turn_rate)
time.sleep(2)
w.stop()

w.turn('cw', turn_rate)
time.sleep(2)
w.stop()

w.turn('ccw', turn_rate)
time.sleep(2)
w.stop()

w.turn('cw', turn_rate)
time.sleep(1)
w.stop()


