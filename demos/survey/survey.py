#!/usr/bin/python

"""
Survey an area
"""

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import signal
import logging
import argparse

import wolfbot as wb
import optitrack

import math
import time

def cleanup(signum, frame):
    w.stop()
    sys.exit()
    outfile.close()

# ugly goto function
def goto(to_z,to_x, dist_eps=0.01, angle_eps=1):
    dist = 99
    while dist > dist_eps:
        position,orientation = opti.get_tracking()
        cur_x,_,cur_z = position
        theta = orientation[0]
        log.debug("Z: %0.3f, X: %0.3f @ %0.2f" % (cur_z,cur_x,theta))

        dx = to_x - cur_x 
        dz = to_z - cur_z

        # NB: ARoS optitrack is calibrated with Y as veritcal and zero
        # To follow right-hand coords, use +z as 0 degrees
        angle = math.atan2(dx,dz) * (180.0/math.pi)
        dist = math.sqrt(dx**2 + dz**2) 

        log.debug("Dist to target: %0.3f" % dist)
        log.debug("Absolute angle to target: %0.2f" % angle)

        angle_rel = angle - theta

        slow = 0.2
        if dist > slow:
            speed = 100
        elif dist > dist_eps:
            speed = 55 + 45 * (dist/slow)
        else:
            speed = 0

        #log.debug("Move: %3.1f @ %0.2f" % (speed, angle_rel))
        w.move(angle_rel,speed)

    ang_target = 0 
    angle = opti.get_orientation()[0]
    ang_dist = ang_target - angle
    while abs(ang_dist) > angle_eps:
        angle = opti.get_orientation()[0]
        ang_dist = ang_target - angle
        if abs(ang_dist) < 180:
            if ang_dist > 0:
                dir = 'ccw'
            else:
                dir = 'cw'
        else:
            if ang_dist > 0:
                ang_dist = 360 - ang_dist
                dir = 'cw'
            else:
                ang_dist += 360
                dir = 'ccw'

        speed = max(25, min(100, 100.0*ang_dist/30.0))
        log.debug("Angle: %0.2f, Turning: %0.1f %s " % (angle, speed, dir))
        w.turn(dir,speed)

#######################

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

parser = argparse.ArgumentParser()
parser.add_argument('target_file', type=str)
parser.add_argument('-o', '--outfile', type=str, default='survey_out.txt')
parser.add_argument('-n', '--num', type=int, default=1)
parser.add_argument('-i', '--id', type=int, default=None)
args = parser.parse_args()

w = wb.wolfbot()
w.log.setLevel(logging.WARN)  # quiet wolfbot internal logging
opti = optitrack.Optitrack()

LOG_FORMAT = '%(asctime)s %(name)s | %(levelname)s | %(message)s'
#logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)
log.info('Startup!')

name = w.config['name']

if args.id:
    wb_id = args.id
else:
    wb_id = w.config['id']

all_targets = []
with file(args.target_file) as tf:
    for line in tf:
        z,x = [float(s) for s in line.split()]
        all_targets.append( (z,x) )
log.info("Read %d total targets" % len(all_targets))

n = args.num
survey_idx =  wb_id % n  # assumes we're using consecutive wolfbots
log.info("Using index %d from WolfBot id %d" % (survey_idx, wb_id))

start = survey_idx * len(all_targets)/n
end = (survey_idx+1) * len(all_targets)/n
bot_targets = all_targets[start : end]
log.info("Surveying targets %d through %d" % (start, end-1))

outfile = file(args.outfile, 'w')
outfile.write("Time WolfBot Target Z X Value\n")

for tid,tgt in enumerate(bot_targets):
    tgt_z = tgt[0]
    tgt_x = tgt[1]
    log.info("Going to: %0.2f, %0.2f" % tgt)
    goto(*tgt, dist_eps=0.03, angle_eps=1)
    log.info("Arrived at: %0.2f, %0.2f" % tgt)

    val = w.lightsensor.adc.read()
    log.info("Survey says: %s" % val)
    # log result
    #position,orientation = opti.get_tracking()
    #x,_,z = position
    outfile.write("%0.2f %s %d %0.2f %0.2f %d\n" % (time.time(), name, tid+start, tgt_z, tgt_x, val))

outfile.close()
w.stop()

