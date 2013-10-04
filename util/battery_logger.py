#!/usr/bin/python -u

""" 
Continuously logs battery level to standard out.

"""

import sys
sys.path.append('/wolfbot/agent')
import wolfbot
import time

log_file = '/sys/class/pwm/pwm7/run'

w = wolfbot.wolfbot()

while True:
  print time.time(), w.battery.voltage() 
  time.sleep(1)
