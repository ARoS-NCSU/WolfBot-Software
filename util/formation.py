#!/usr/bin/python

import sys
import argparse
import importlib

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot
import optitrack
from movelib import goto_and_stop

parser = argparse.ArgumentParser()
parser.add_argument('name')
parser.add_argument('-p', '--params')
parser.add_argument('-o', '--offset', type=int, default=0)
parser.add_argument('-c', '--count', type=int, default=11)
parser.add_argument('-s', '--start', type=float, default=0.0)
parser.add_argument('-e', '--end', type=float, default=1.0)
parser.add_argument('-l', '--loop', action='store_true', default=False, 
        help = 'Augment spacing to avoid overlap in looped formations')
parser.add_argument('-d', '--debug', action='store_true', default=False)
args = parser.parse_args()

count = args.count
offset = args.offset
start = args.start
end = args.end
name = args.name

wb = wolfbot.wolfbot()


index = (wb.config['id']+args.offset) % count
print "Index: #{} from 0-{}".format(index,count-1)

func_range = end-start

if args.loop:
    # indexes still 0 - (count-1)
    # but spread size is now based on count (not count-1)
    # but we still start at beginning of range
    #  3 4 5 6 1 2 X  (noone has the highest slot, which overlaps with lowest)
    scaled = start + func_range * float(index)/count
else:
    scaled = start + func_range * float(index)/(count-1)
print "Scaled: {:0.3} in range [{},{}]".format(scaled,start,end)

formation = importlib.import_module('formations.%s' % name)
try:
    if args.params:
        params = map(float,args.params.split(","))
        print "Params: ", params
        x,y,theta = formation.pose(scaled, params)
    else:
        x,y,theta = formation.pose(scaled)
    print "Pose: ({:0.2f},{:0.2f}) @ {}".format(x,y,theta)
except TypeError:
    print "Wrong parameters for pose function"
    exit()

opti = optitrack.Optitrack()
try:
    goto_and_stop(wb, x, y, theta, opti.get_pose)
except KeyboardInterrupt:
    wb.stop()
