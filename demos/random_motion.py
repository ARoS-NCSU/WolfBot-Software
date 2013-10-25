#!/usr/bin/python

import sys, os
import logging
import argparse
import signal

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot as wb
import optitrack
import simple_move

import time
from math import degrees, radians, sin, cos, atan2, sqrt
import random

# change to atexit?
def cleanup(signum, frame):
    log.critical("Received signal %d" % signum)
    w.stop()
    log.info("Exiting")
    # for some reason sys.exit() and quit() don't always work
    os._exit(0)

def sensor_force():
    dms = w.dms_mux.read_all()
    z_tot = 0.0
    x_tot = 0.0
    for name, val in sorted(dms.items()):
        #angle = 360 - name
        angle = name
        log.debug("Sensor: {:3}, value: {:4}".format(angle, val))

        if val > 800:
            val = 800
        z = val * cos(radians(angle))
        x = val * sin(radians(angle))
        z_tot += z
        x_tot += x

    log.debug("sensor total: z: %0.2f, x: %0.2f" % (z_tot, x_tot))
    mag = 100 * (abs(z_tot) + abs(x_tot))/800  # normalize to ??
    angle = degrees(atan2(x_tot, z_tot)) % 360
    log.debug("sensor force: mag: %6.2f, angle: %5.1f" % (mag, angle))
    return angle, mag

# TODO: Faking sensor respose like this would be better handled by swapping the
# wolfbot's dms objects with a class that responds in the desired way.  For
# example, a sensor which is initialized with map data and a localizer function
# (e.g.  optitrack.get_pose)
def wall_force(coords):

    def dist2sensor(pos, limit, range, max_val):
        #log.debug("dist2sensor(pos={:0.3f}, limit={:0.3f}, range={}, max={})".format(pos, limit, range, max_val))
        if pos > limit:
            val =  max_val
        elif pos < (limit - range):
            val = 0
        else:
            # inversely proportional to distance from limit
            val = max_val * (range - (limit-pos))/range
        
        #log.debug("dist2sensor: val = %0.2f", val)
        return val

    sensor_range = 0.2  # meters
    sensor_min = 0
    sensor_max = 500

    z_min = coords[0]
    z_max = coords[2]
    x_min = coords[1]
    x_max = coords[3]

    pose = opti.get_pose()

    z_vec = 0
    x_vec = 0

    # test each virtual wall: +Z, -Z, +X, -X
    z_vec += dist2sensor( pose['z'], z_max, sensor_range, sensor_max )
    z_vec -= dist2sensor( z_min, pose['z'], sensor_range, sensor_max )
    x_vec += dist2sensor( pose['x'], x_max, sensor_range, sensor_max )
    x_vec -= dist2sensor( x_min, pose['x'], sensor_range, sensor_max )

    log.debug("Wall force: z_vec %0.2f, x_vec: %0.2f" % (z_vec, x_vec))

    mag = 100 * (abs(z_vec) + abs(x_vec)) / sensor_max
    angle = norm_angle( degrees(atan2(x_vec, z_vec)) )
    log.debug("global wall force: mag: %6.2f, angle: %5.1f" % (mag, angle))
    # TODO adjust angle to be relative to wolfbot, not global
    angle = norm_angle( angle - pose['yaw'] )
    log.debug("relative wall force: mag: %6.2f, angle: %5.1f" % (mag, angle))

    return angle, mag


def bounce_box( angle, mag, coords = [-1.5, -1.25, 1.15, 1.65]):
    """ Stay within a bounding box

    coords : 
    angle : the relative angle we're supposedly traveling in
    coords : bounding box [z_min, x_min, z_max, x_max]

    """

    log.debug("Call: bounce_box({:0.1f},{},{})".format(angle,mag, coords))
    min_z = coords[0]
    max_z = coords[2]
    min_x = coords[1]
    max_x = coords[3]
    pose = opti.get_pose()
    log.debug("Pose: ({z:0.2},{x:0.2}) @ {yaw:0.1f}".format(**pose))
    log.debug("Relative angle {:0.1f}".format(angle))
    global_angle = norm_angle(angle + pose['yaw'])
    z_vec = cos(radians(global_angle))
    x_vec = sin(radians(global_angle))
    log.debug("Global angle %0.1f (z: %0.1f, x: %0.1f)" % (global_angle, z_vec, x_vec))
   
    mod = 0.2
    if pose['z'] < min_z:
        log.info("Outside -Z bound, forcing positive")
        #z_vec = abs(z_vec)
        z_vec += mod
    if pose['z'] > max_z:
        log.info("Outside +Z bound, forcing negative")
        #z_vec = -abs(z_vec)
        z_vec -= mod
    if pose['x'] < min_x:
        log.info("Outside -X bound, forcing positive")
        #x_vec = abs(x_vec)
        x_vec += mod
    if pose['x'] > max_x:
        log.info("Outside +X bound, forcing negative")
        #x_vec = -abs(x_vec)
        x_vec -= mod
    
    new_global_angle = degrees(atan2(x_vec,z_vec))
    log.debug("New global angle %0.1f (z: %0.1f, x: %0.1f)" % (new_global_angle, z_vec, x_vec))
    new_angle = norm_angle(new_global_angle - pose['yaw'])
    log.debug("New relative angle %0.1f", new_angle)
    w.move(new_angle,mag)

    return new_angle,mag


def sensor_box( angle, mag, coords = [-1.5, -1.25, 1.15, 1.65]):
    """ combine sensor and bounding box 'forces' together """

    log.debug("Call: sensor_box({},{},{})".format(angle, mag, coords))

    sensor_angle, sensor_mag = sensor_force()
    wall_angle, wall_mag = wall_force(coords)

    force_z = sensor_mag * cos(radians(sensor_angle)) + wall_mag * cos(radians(wall_angle))
    force_x = sensor_mag * sin(radians(sensor_angle)) + wall_mag * sin(radians(wall_angle))
    log.debug("forces: z: %0.2f, x: %0.2f" % (force_z, force_x))

    # influence current trajectory
    z_tot = mag * cos(radians(angle)) - force_z
    x_tot = mag * sin(radians(angle)) - force_x
    log.debug("total: z: %0.2f, x: %0.2f" % (z_tot, x_tot))

    new_angle = degrees(atan2(x_tot, z_tot))
    new_mag = min(100, sqrt(abs(z_tot)**2 + abs(x_tot)**2) )
    # accel if we're not running into anything serious
    if sqrt(force_z**2 + force_x**2) < 30:
        new_mag = min(100, new_mag+10)

    log.debug("New: %0.1f @ %0.1f", new_mag, new_angle)
    w.move(new_angle, new_mag)
    return new_angle, new_mag

    ## foo

    away_angle = degrees(atan2(x_tot, z_tot))
    away_angle = norm_angle( (away_angle + 180) % 360 )
    away_mag = min(100, abs(z_tot) + abs(x_tot))

    if away_mag > 50:
        log.debug("Away: %0.1f @ %0.1f", away_mag, away_angle)
        w.move(away_angle, away_mag)
        return away_angle, away_mag
    else:
        #mag = min(100, 
        #w.stop()
        mag = min(100, mag+10)
        log.debug("Continue: %0.1f @ %0.1f", mag, angle)
        w.move(angle, mag)
        return angle, mag
        

def norm_angle(angle):
    """ Normalize an angle in degrees to the range (-180,180] """
    new_angle = angle % 360  # [0,360)
    if new_angle > 180:
        new_angle -= 360  # (-180,180]
    if abs(new_angle - angle) > 1:
        log.debug("Normalized {} to {}".format(angle, new_angle))
    return new_angle

#####################################################

if __name__ == '__main__':

    w = wb.wolfbot()
    w.log.setLevel(logging.WARN)
    opti = optitrack.Optitrack()

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true', default=False)
    args = parser.parse_args()

    LOG_FORMAT = '%(asctime)s %(name)s | %(levelname)s | %(message)s'
    if args.debug:
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    else:
        logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Startup!')

    angle = 90
    mag = 100
    w.move(angle,mag)

    #simple_move.goto(w, 0, 0, 0, opti.get_pose)
    while True:

        #angle, mag = shy(*sensor_force())

        # safe area at approx (z,x) : (-1.60, -1.25) - (+1.15, +1.65)
        #angle,mag = bounce_box(angle, mag, coords=[-1.6, -1.25, 0.0, 0.0])

        angle, mag = sensor_box(angle, mag, coords = [-1.0, -1.0, 1.0, 1.0])
        log.info("Moving: %0.1f @ %0.1f", mag, angle)

