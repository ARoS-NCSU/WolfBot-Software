#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot

import argparse
import time
import math
import signal
import os
from random import uniform as rand

# TODO:
# filter samples
# reset straight timer
# lower sensitivity
# longer straight time

def cleanup(signum, frame):
    adc_file.close()
    obs_file.close()
    wb.stop()
    os._exit(0)

def check_dists(dists, min_dist):
    min_sensor = 0
    for sensor in wb.dms:
        reading = dists[sensor]
        if reading <= dists[min_sensor]:
            min_sensor = sensor 
    if dists[min_sensor] < min_dist:
        return min_sensor  #returns value only if obstacle in range
    else: 
        return None

def avoid(sensor, away_range):
    away_sensor = (sensor + 180) % 360
    half = away_range / 2.0
    away_angle = rand(away_sensor-half, away_sensor+half)
    debug("Centering avoidance at %d, random angle %0.2f" % (away_sensor, away_angle))
    wb.move(away_angle)

def record_adcs(file,dists):
    dist_strings = [str(dists[i]) for i in sorted(dists)]
    rel_time = time.time() - t0
    file.write( ('%.3f, ' % rel_time) + ', '.join(dist_strings)+'\n')

def datafile(base):
    prefix = '/root/'
    suffix = '_%s_%s.txt' % (wb.hostname, time.strftime("%Y-%m-%d-%H:%M"))
    filename = prefix + base + suffix
    f = open(filename, 'w')

    f.write('System Time: %.4f (%s)\n' % (time.time(),time.ctime()))
    f.write('time, D_000, D_060, D_120, D_180, D_240, D_300\n')
    return f

def debug(msg):
    if debug_on:
        print "%0.4f" % (time.time() - t0), wb.hostname, msg

def verify(sensor, min_dist, count):
    debug("Verifying %d times" % count)
    for i in range(count):
        dist = wb.dms[sensor].read(mode='inch')
        if dist > min_dist:
            debug("Verifying failed on read %d : dist = %0.2f" % (i, dist)) 
            return False
    return True

###########################################

if __name__ == '__main__':

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    parser = argparse.ArgumentParser()
    parser.add_argument('runtime', type=float, default=0.0)
    parser.add_argument('-x', dest='excludes', help='Exclude bots from motion by number')
    parser.add_argument('--dist', dest='min_dist', type=float, default = 6.0,
            help='Closest sensor distance before avoid (inches)')
    parser.add_argument('--amin', dest='avoid_min', type=float, default = 0.25,
            help='Min time to avoid before rechecking avoidance (secs)')
    parser.add_argument('--mmax', dest='move_max', type=float, default = 7.5,
            help='Max time to move striaght before random change (secs)')
    parser.add_argument('--arange', dest='away_range', type=float, default = 160,
            help='Random range for bounce angle (degrees)')
    parser.add_argument('--verify', dest='verify_count', type=int, default = 1,
            help='Random range for bounce angle (degrees)')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False)
    args = parser.parse_args()

    debug_on = args.debug
    static_nodes = []
    if args.excludes:
        static_nodes = [int(x) for x in args.excludes.split(",")]

    wb = wolfbot.wolfbot()

    adc_file = datafile('adc_stream')
    obs_file = datafile('obstacle_times')

    wb_id = wb.config['id']
    dists = []

    t0 = time.time()
    move_start = 0
    avoid_start = t0 - args.avoid_min  # allow wolfbot to avoid immediately
    while (time.time() - t0) < args.runtime:

        dists = wb.dms_mux.read_all(mode='inch')
        record_adcs(adc_file,dists)

        now = time.time()
        if wb_id not in static_nodes:
            if (now - move_start) > args.move_max:
                debug("Reached max move, chosing random direction")
                wb.move(rand(0,360))
                move_start = now

        sensor = check_dists(dists, args.min_dist)    # TODO: add filtering
        if (sensor is not None):
            debug("Tripped sensor %d (%0.2f in)" % (sensor, dists[sensor]))
            if not verify(sensor, args.min_dist, args.verify_count):
                debug("FALSE reading detected, ignoring!")
                continue
            if (now - move_start) > args.avoid_min:
                record_adcs(obs_file,dists)
                debug("Avoiding away from %d!" % sensor)
                if wb_id not in static_nodes:
                    avoid(sensor, args.away_range)
                    move_start = now
                    avoid_start = now
                else:
                    debug("Static node, not avoiding")
            else:
                debug("Ignoring sensor, avoid started %0.2fs ago" %(now-avoid_start))

    debug("Time up!")
    wb.stop()



