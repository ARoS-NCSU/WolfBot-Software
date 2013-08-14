#!/usr/bin/python

import wolfbot as wb
import time

w = wb.wolfbot()

#delay each bot by id amout
#n = w.config['id']
#time.sleep(n)
w.move(30,150)
time.sleep(1)
w.move(180,150)
time.sleep(1)
w.move(330,150)

w.stop()

#turn("cc")
#turn("cw")
