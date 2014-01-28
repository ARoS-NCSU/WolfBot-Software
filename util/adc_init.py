#!/usr/bin/python

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import wolfbot as wb
import time
import optitrack
import simple_move
import math

from simple_move import goto as move

w = wb.wolfbot()
opti = optitrack.Optitrack()
pose = opti.get_pose

move(w,-1.32,0.831,180,pose)
adc6in000 = w.dms[0].read()
print "D_000 reads ", adc6in000," at 6 inches."
move(w,-1.32,0.831,120,pose)
adc6in060 = w.dms[60].read()
print "D_060 reads ", adc6in060," at 6 inches."
move(w,-1.32,0.831,60,pose)
adc6in120 = w.dms[120].read()
print "D_120 reads ", adc6in120," at 6 inches."
move(w,-1.32,0.831,0,pose)
adc6in180 = w.dms[180].read()
print "D_180 reads ", adc6in180," at 6 inches."
move(w,-1.32,0.831,300,pose)
adc6in240 = w.dms[240].read()
print "D_240 reads ", adc6in240," at 6 inches."
move(w,-1.32,0.831,240,pose)
adc6in300 = w.dms[300].read()
print "D_300 reads ", adc6in300," at 6 inches."

move(w,-1.0062,0.831,180,pose)
adc12in000 = w.dms[0].read()
print "D_000 reads ", adc12in000," at 12 inches."
move(w,-1.0062,0.831,120,pose)
adc12in060 = w.dms[60].read()
print "D_060 reads ", adc12in060," at 12 inches."
move(w,-1.0062,0.831,60,pose)
adc12in120 = w.dms[120].read()
print "D_120 reads ", adc12in120," at 12 inches."
move(w,-1.0062,0.831,0,pose)
adc12in180 = w.dms[180].read()
print "D_180 reads ", adc12in180," at 12 inches."
move(w,-1.0062,0.831,300,pose)
adc12in240 = w.dms[240].read()
print "D_240 reads ", adc12in240," at 12 inches."
move(w,-1.0062,0.831,240,pose)
adc12in300 = w.dms[300].read()
print "D_300 reads ", adc12in300," at 12  inches."

# Slope, m, formula: y=mx+b
m000 = (adc12in000 - adc6in000)/6 #div by 6 inches
m060 = (adc12in060 - adc6in060)/6 
m120 = (adc12in120 - adc6in120)/6 
m180 = (adc12in180 - adc6in180)/6 
m240 = (adc12in240 - adc6in240)/6 
m300 = (adc12in300 - adc6in300)/6 

# Y-intercept, b: y=mx+b
b000 = adc6in000 - m000*6
b060 = adc6in060 - m060*6
b120 = adc6in120 - m120*6
b180 = adc6in180 - m180*6
b240 = adc6in240 - m240*6
b300 = adc6in300 - m300*6

print
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print
print w.hostname

print "ADC angle 000, slope: ", m000, " , x intercept: ", b000
print "ADC angle 060, slope: ", m060, " , x intercept: ", b060
print "ADC angle 120, slope: ", m120, " , x intercept: ", b120
print "ADC angle 180, slope: ", m180, " , x intercept: ", b180
print "ADC angle 240, slope: ", m240, " , x intercept: ", b240
print "ADC angle 300, slope: ", m300, " , x intercept: ", b300

w.stop()

