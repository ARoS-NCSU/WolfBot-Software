#!/usr/bin/python

"""
Silly demo that centers a wolfbot from Optitrack feedback.  
Needs to be rewritten with a proper PID controller.
"""

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot as wb
import optitrack

w = wb.wolfbot()
opti = optitrack.Optitrack()

while True:
    track = opti.get_tracking()
    yaw = track[0]
    #print "Yaw: ", yaw
    if abs(yaw) < 3:
        w.stop()
    elif yaw > 0:
        # too positive, go cw
        speed = 100.0*yaw/180
        if speed < 30:
            speed = 30
        #print"  CW : ", speed
        w.turn('cw',speed)
    elif yaw < 0:
        # too negative, go ccw
        speed = 100.0*-yaw/180
        if speed < 30:
            speed = 30 
        #print"  CCW: ", speed
        w.turn('ccw',speed)

