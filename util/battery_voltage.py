#!/usr/bin/python -u

import sys
sys.path.append('/wolfbot/agent')
import wolfbot
import time

w = wolfbot.wolfbot()

print "%0.2f" % w.battery.voltage() 
