#!/usr/bin/python

import wolfbot as wb
import slicer
import ir
import atexit

w = wb.wolfbot()

atexit.register(ir.ir_off)
s = slicer.slicer(w)

while True:
  s.sleep_until_start()  # wait for our next full slice
  ir.ir_pulse(s.slice_ms)

