#!/usr/bin/python

"""
Simple (or at least naive) movement library.

Move to specified pose based on feedback from a localization function that
provides global pose information.

"""

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import logging
import argparse

import wolfbot as wb
import optitrack

import math
import time

# ugly goto function
# localizer should return (x,y,z,yaw,pitch,roll)
def goto(w, to_z, to_x, to_theta, localizer, dist_eps=0.01, angle_eps=1):

    log = logging.getLogger(__name__)
    log.info("Moving to z: %0.2f, x: %0.2f (+/- %0.3f)" % (to_z,to_x,dist_eps))
    dist = 99
    prev_dist = 99
    bonus = 0
    while dist > dist_eps:
        pose = localizer()
        log.debug("Z: %0.3f, X: %0.3f @ %0.2f" % (pose['z'],pose['x'],pose['yaw']))

        dx = to_x - pose['x']
        dz = to_z - pose['z']

        # NB: ARoS optitrack is calibrated with Y as veritcal and zero
        # To follow right-hand coords, use +z as 0 degrees
        angle = math.atan2(dx,dz) * (180.0/math.pi)
        dist = math.sqrt(dx**2 + dz**2) 
        angle_rel = angle - pose['yaw']

        log.debug("Dist to target: %0.3f @ %0.1f (rel) or %0.1f (global)" % (dist, angle_rel, angle))

        slow = 5*dist_eps
        if dist > slow:
            speed = 100
        elif dist > dist_eps:
            speed = (dist/slow)*100
        else:
            speed = 0

        if prev_dist - dist < 0.003:
            bonus += 5 
            log.debug("Stall in move, bonus now: %0.1f" % bonus )
        else:
            bonus = 0
        speed += bonus

        speed = min(100,speed)

        log.debug("Moving: %3.1f @ %0.2f" % (speed, angle_rel))
        w.move(angle_rel,speed)
        prev_dist = dist

    log.info("Turning to: %0.1f (+/- %0.1f)" % (to_theta,angle_eps))
    ang_dist = 999
    prev_dist = 999
    bonus = 0
  
    to_theta %= 360  # [0,360)
    if to_theta > 180:
        to_theta -= 360  # (-180,180]

    while abs(ang_dist) > angle_eps:
        angle = localizer()['yaw']
        ang_dist = to_theta - angle
        # TODO(jcschorn): would it be simpler just to normalize ang_dist to (-180,180]?
        if abs(ang_dist) < 180:
            if ang_dist > 0:
                dir = 'ccw'
            else:
                dir = 'cw'
                ang_dist = -ang_dist
        else:
            if ang_dist > 0:
                ang_dist = 360 - ang_dist
                dir = 'cw'
            else:
                ang_dist += 360
                dir = 'ccw'
        try:
            assert 0 <= ang_dist <= 180
        except AssertionError:
            log.warning("Angle: %0.1f, to_theta: %0.1f => ang_dist = %0.1f (%s)", 
                    angle, to_theta, ang_dist, dir)

        slow = 75*angle_eps
        if ang_dist > slow:
            speed = 100
        elif ang_dist > angle_eps:
            speed = (ang_dist/slow)*100
        else:
            speed = 0

        if prev_dist - ang_dist < 0.3:
            bonus += 5 
            log.debug("Stall during turn, bonus now: %0.1f" % bonus )
        else:
            bonus = 0
        speed = min(100,speed+bonus)

        log.debug("Angle: %0.2f, Turning: %0.1f %s " % (angle, speed, dir))
        w.turn(dir,speed)
        prev_dist = ang_dist

    w.stop()
    log.info("Final position: {z:0.2f}, {x:0.2f} @ {yaw:0.1f}".format(**localizer()))


