#!/usr/bin/python

import sys
import argparse

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot as wb
import optitrack
import simple_move
import math

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', type=int, default=4)
parser.add_argument('-s', '--size', type=float, default=2.0)
args = parser.parse_args()

n = args.num
size = args.size

w = wb.wolfbot()
opti = optitrack.Optitrack()

per_side = int(round(math.sqrt(n)))
spacing = size / (per_side-1)

z_i = w.config['id'] % per_side
x_i = (w.config['id'] % n) / per_side


print "Num: ", n
print "Per side: ", per_side


print "Size: ", size 
print "Spacing: ", spacing
print
print "z_i: ", z_i
print "x_i: ", x_i

if per_side % 2:  # odd
    offset = 0
    print "No offset"
else:
    offset = 1
    print "Using offset"

z = -size/2 + spacing*z_i
x = -size/2 + spacing*x_i

print
print "z: ", z
print "x: ", x

try:
    simple_move.goto(w, z, x, 0, opti.get_pose)
except KeyboardInterrupt:
    w.stop()
