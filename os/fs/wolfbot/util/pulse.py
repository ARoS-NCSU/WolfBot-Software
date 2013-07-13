#!/usr/bin/python

""" 
A slightly improve burst generator for the IR PWM signal.

This gives us roughly a 500us burst (~30 cycles) of 56kHz every ~2ms (500 Hz)

Optimally, we'd like 360us (20 cylces) every 1.3ms (750 Hz), but that level 
of precision likely requires the use of hardware timers.  Some minor improvement
may also be possible with a C implementation.
   
"""

import signal, sys
from time import sleep

pwm_run = '/sys/class/pwm/pwm7/run'

def cleanup(signum, frame):
  run = open(pwm_run, 'w')
  run.write('0\n')  
  run.close()
  sys.exit()

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

while True:
  run = open(pwm_run, 'w')
  run.write('1\n')  
  run.close()
  #sleep(0.001)  # 

  run = open(pwm_run, 'w')
  run.write('0\n')  
  run.close()
  sleep(0.001)
