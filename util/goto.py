#!/usr/bin/python

"""
Silly demo that moves a wolfbot based on Optitrack feedback.  
"""

import sys
import signal
import argparse
import logging

sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot as wb
import optitrack
import simple_move

import math

parser = argparse.ArgumentParser()
parser.add_argument('z', type=float, default=0.0)
parser.add_argument('x', type=float, default=0.0)
parser.add_argument('theta', type=float, default=0.0)
parser.add_argument('-d' , '--debug', action='store_true', default=False)
args = parser.parse_args()

LOG_FORMAT = '%(asctime)s %(name)s | %(levelname)s | %(message)s'
if args.debug:
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
else:
    logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)
log.info('Startup!')

opti = optitrack.Optitrack()

w = wb.wolfbot()
w.log.setLevel(logging.WARN)

def cleanup(signum, frame):
    w.stop()
    sys.exit()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

simple_move.goto(w,args.z, args.x, args.theta, opti.get_pose)

