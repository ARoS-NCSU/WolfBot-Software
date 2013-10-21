#!/usr/bin/python

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
parser.add_argument('theta', type=float, default=0.0)
parser.add_argument('-d' , '--debug', action='store_true', default=False)
args = parser.parse_args()

def cleanup(signum, frame):
    w.stop()
    sys.exit()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

target = args.theta
target = target % 360

while True:

    print "Target: ", target
    orientation = opti.get_orientation()
    angle = orientation[0] % 360
    print "Angle: ", angle

    epsilon = 3
    slow = 100 
    diff = target - angle
    print "Raw Diff: ", diff
    if abs(diff) < 180:
        if diff > 0:
            dir = 'ccw'
        else:
            dir = 'cw'
    else:
        if diff > 0:
            diff = 360 - diff
            dir = 'cw'
        else:
            diff = 360 + diff
            dir = 'ccw'

    print "Actual diff: ", diff

    if abs(diff) > slow:
        speed = 100
    elif abs(diff) > epsilon:
        speed = 25 + 75 * (abs(diff)/slow)
    else:
        speed = 0

    print "Turn %s %0.2f" % (dir, speed)
    w.turn(dir, speed)

    print
