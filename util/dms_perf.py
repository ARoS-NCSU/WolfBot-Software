#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--num', type=int, default=100)
args = parser.parse_args()
num = args.num

wb = wolfbot.wolfbot()

print "ADC repeat setting: ", wb.dms_mux.adc.repeat
print "Reading all sensors {} times...".format(num)
t0 = time.time()
for i in range(num):
    dms = wb.dms_mux.read_all()
elapsed = time.time() - t0
time_each = elapsed/num
rate_hz = 1.0/time_each
print "Took {:0.2f} secs, ({:0.2f} ms/ea, {:0.2f} Hz)".format(elapsed, time_each*1000, rate_hz)

