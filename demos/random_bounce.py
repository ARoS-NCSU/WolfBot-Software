#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')

import wolfbot as wb
import time
import math
from random import uniform as rand

w = wb.wolfbot()
max_adc = 500
quick_sleep = 0.5

def check_dist():
	for i in range(6):
		sensor = i*60
		if w.dms[sensor].read() > max_adc:
			return(sensor)

def avoid(sensor):
	away_angle = sensor+180	
	w.move(rand(away_angle-90, away_angle+90))

sixft_time = 7.5 #estimates how long it takes bot to travel 6 ft
run_time = 30  #how long in seconds to run experiment
t0 = time.time() #set initial time of experiment

while (time.time()-t0) < run_time:
	t_path = time.time()
	w.move(rand(0,360))
	while (time.time() - t_path) < sixft_time:	
		sensor = check_dist()
		if sensor != None:
			avoid(sensor)
			t_path = time.time()	
			time.sleep(quick_sleep)	
	
w.stop()







w.stop()
