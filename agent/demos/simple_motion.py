#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
import wolfbot as wb
import time

w = wb.wolfbot()

#n = w.config['id']
#time.sleep(n)

w.move(90,100)
time.sleep(1.5)
w.stop()
time.sleep(0.2)

w.move(-90,100)
time.sleep(3.0)
w.stop()
time.sleep(0.2)

w.move(90,100)
time.sleep(1.5)
w.stop()
time.sleep(0.2)


##########
w.turn('cw', 100)
time.sleep(2)
w.stop()
time.sleep(0.2)

w.turn('ccw', 100)
time.sleep(2)
w.stop()
time.sleep(0.2)

##########
w.move(90,100)
time.sleep(1.5)
w.stop()
time.sleep(0.1)

w.move(180,100)
time.sleep(1.5)
w.stop()
time.sleep(0.1)

w.move(270,100)
time.sleep(1.5)
w.stop()
time.sleep(0.1)

w.move(0,100)
time.sleep(1.5)
w.stop()
time.sleep(0.1)


w.stop()

