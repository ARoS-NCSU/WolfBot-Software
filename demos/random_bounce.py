#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')

import wolfbot as wb
import time
import math
from random import uniform as rand

w = wb.wolfbot()
f = open('obstacle_times.txt', 'w')
max_adc = 500
quick_sleep = 0.5
sixft_time = 7.5 #estimates how long it takes bot to travel 6 ft
run_time = 30  #how long in seconds to run experiment
t0 = time.time() #set initial time of experiment
f.write('Epoch: %.4f\n' %t0)

def check_dist():
	max_sensor = 0
	for i in range(6):
		sensor = i*60
		reading = w.dms[sensor].read()
		if reading >= w.dms[max_sensor].read():
			max_sensor = sensor 
	if w.dms[max_sensor].read() > max_adc:
		return(max_sensor)

def avoid(sensor):
	away_angle = sensor+180	
	w.move(rand(away_angle-80, away_angle+80))
	f.write('%.4f\n' %(time.time()-t0))

while 1:
	t_path = time.time()
	w.move(rand(0,360))
	while (time.time() - t_path) < sixft_time:	
		if (time.time()-t0) >= run_time:
			w.stop()
			f.close()
			exit()
		sensor = check_dist()
		if sensor != None:
			avoid(sensor)
			t_path = time.time()	
			time.sleep(quick_sleep)	
	
w.stop()
f.close()
exit()
