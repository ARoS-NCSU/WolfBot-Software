#!/usr/bin/python

"""
Dump Optitrack pose information received form the proxy
"""

import sys

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import optitrack

opti = optitrack.Optitrack()

print "Optitrack reports: z: {z:0.3f}, x: {x:0.3f}, yaw: {yaw:0.2f}".format(**opti.get_pose())
