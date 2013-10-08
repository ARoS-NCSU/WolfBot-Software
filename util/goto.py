#!/usr/bin/python

"""
Silly demo that moves a wolfbot based on Optitrack feedback.  
"""

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import signal

import wolfbot as wb
import optitrack

import argparse
import math


w = wb.wolfbot()
opti = optitrack.Optitrack()

parser = argparse.ArgumentParser()
parser.add_argument('z', type=float, default=0.0)
parser.add_argument('x', type=float, default=0.0)
parser.add_argument('-d' , '--debug', action='store_true', default=False)
args = parser.parse_args()

z_target = args.z
x_target = args.x

def cleanup(signum, frame):
    w.stop()
    sys.exit()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

while True:
    position,orientation = opti.get_tracking()
    x,y,z = position
    theta = orientation[0]
    print "X: %0.3f, Y: %0.3f, Z: %0.3f @ %0.2f" % (x,y,z,theta)


    dx = x_target - x
    dz = z_target - z

    # NB: ARoS optitrack is calibrated with Y as veritcal and zero
    # To follow right-hand coords, use +z as 0 degrees
    angle = math.atan2(dx,dz) * (180.0/math.pi)
    dist = math.sqrt(dx**2 + dz**2) 

    print "Dist to target: %0.3f" % dist
    print "Absolute angle to target: %0.2f" % angle

    angle_rel = angle - theta

    epsilon = 0.003
    slow = 0.1
    if dist > slow:
        speed = 100
    elif dist > epsilon:
        speed = 50 + 50 * (dist/slow)
    else:
        speed = 0

    print "Move: %3.1f @ %0.2f" % (speed, angle_rel)
    w.move(angle_rel,speed)

    print


