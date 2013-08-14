#!/usr/bin/python

import wolfbot as wb
import time

w = wb.wolfbot()

#n = w.config['id']
#time.sleep(n)
w.move(0,100)
time.sleep(1.5)
w.move(90,100)
time.sleep(1.5)
w.move(180,100)
time.sleep(1.5)
w.move(270,100)
time.sleep(1.5)
w.stop()

