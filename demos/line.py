#!/usr/bin/python

# TODO: Define a function that returns an X,Y,theta along its range, and feed
# it into a generic function that disperses discrete wolfbots along it

import sys
import argparse

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot as wb
import optitrack
import simple_move
import math

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--offset', type=int, default=0)
parser.add_argument('-c', '--count', type=int, default=10)
parser.add_argument('-z', '--zpos', type=float, default=0.0)
parser.add_argument('-x', '--xpos', type=float, default=None)
parser.add_argument('-s', '--spread', type=float, default=2.5)
parser.add_argument('-a', '--angle', type=float, default=0.0)
args = parser.parse_args()

count = args.count
spread = args.spread

w = wb.wolfbot()
opti = optitrack.Optitrack()

spacing = spread / (count-1)

x_i = ( (w.config['id']+args.offset) % count)

print "Num: ", count
print "Size: ", spread
print "Spacing: ", spacing
print
print "x_i: ", x_i

if args.xpos is not None:
	x = args.xpos
	z = -spread/2 + spacing*x_i
else:
	z = args.zpos
        x = -spread/2 + spacing*x_i

print
print "z: ", z, "x: ", x

try:
    simple_move.goto(w, z, x, args.angle, opti.get_pose)
except KeyboardInterrupt:
    w.stop()
