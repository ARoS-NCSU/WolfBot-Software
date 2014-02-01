#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')

import argparse
import wolfbot as wb
import time
import math
import signal 
import os
from random import uniform as rand

parser = argparse.ArgumentParser()
parser.add_argument('runtime', type=float, default=0.0)
args = parser.parse_args()
w = wb.wolfbot()

timestring = time.strftime("_%Y_%m_%d_%H%M")
obsfile = '/root/obstacle_times_'+w.hostname+timestring+'.txt'
adcfile = '/root/adc_stream_'+w.hostname+timestring+'.txt'
obs_write = open(obsfile, 'w')
adc_write = open(adcfile, 'w')

max_adc = 500
quick_sleep = 0.5
sixft_time = 7.5 #estimates how long it takes bot to travel 6 ft
run_time = args.runtime  #how long in seconds to run experiment
t0 = time.time() #set initial time of experiment

def cleanup(signum, frame):
	w.stop()
    	os._exit(0)

def check_dist():
	max_sensor = 0
	vals = w.dms_mux.read_all()
        read_all_string = [str(vals[i]) for i in sorted(vals)]
        t = time.time()-t0
        adc_write.write('%.3f, '%t+', '.join(read_all_string)+'\n')
	for i in range(6):
		sensor = i*60
		reading = vals[sensor]
		if reading >= vals[max_sensor]:
			max_sensor = sensor 
	if vals[max_sensor] > max_adc:
		return(max_sensor) #returns value only if obstacle in range
	else: 
		return None

def avoid(sensor):
	away_angle = sensor+180	
	w.move(rand(away_angle-80, away_angle+80))
        # vals = w.dms_mux.read_all()
        read_all_string = [str(vals[i]) for i in sorted(vals)]
	t = time.time()-t0
	obs_write.write('%.3f, '%t+', '.join(read_all_string)+'\n')

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)
vals = {}
obs_write.write('Epoch Time: %.4f\n' %t0)
adc_write.write('Epoch Time: %.4f\n' %t0)
obs_write.write('time, D_000, D_060, D_120, D_180, D_240, D_300\n')
adc_write.write('time, D_000, D_060, D_120, D_180, D_240, D_300\n')

while 1:
	t_path = time.time()
	w.move(rand(0,360))
	while (time.time() - t_path) < sixft_time:	
		if (time.time()-t0) >= run_time:
			w.stop()
			obs_write.close()
			adc_write.close()
			exit()
		sensor = check_dist()
		if sensor != None:
			avoid(sensor)
			t_path = time.time()	
			time.sleep(quick_sleep)	
	
w.stop()
obs_write.close()
adc_write.close()
exit()
