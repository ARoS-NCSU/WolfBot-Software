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
a =  w.dms[0].read() 
move(w,-1.32,0.831,180,pose)
b =  w.dms[0].read()
move(w,-1.32,0.831,180,pose)
c =  w.dms[0].read()
adc6in000 = (a+b+c)/3
print "D_000 reads ", adc6in000," at 6 inches."

move(w,-1.32,0.831,120,pose)
a =  w.dms[60].read()
move(w,-1.32,0.831,120,pose)
b = w.dms[60].read()
move(w,-1.32,0.831,120,pose)
c = w.dms[60].read()
adc6in060 = (a+b+c)/3
print "D_060 reads ", adc6in060," at 6 inches."

move(w,-1.32,0.831,60,pose)
a = w.dms[120].read()
move(w,-1.32,0.831,60,pose)
b = w.dms[120].read()
move(w,-1.32,0.831,60,pose)
c = w.dms[120].read()
adc6in120 = (a+b+c)/3
print "D_120 reads ", adc6in120," at 6 inches."

move(w,-1.32,0.831,0,pose)
a = w.dms[180].read()
move(w,-1.32,0.831,0,pose)
b = w.dms[180].read()
move(w,-1.32,0.831,0,pose)
c = w.dms[180].read()
adc6in180 = (a+b+c)/3
print "D_180 reads ", adc6in180," at 6 inches."

move(w,-1.32,0.831,300,pose)
a = w.dms[240].read()
move(w,-1.32,0.831,300,pose)
b = w.dms[240].read()
move(w,-1.32,0.831,300,pose)
c = w.dms[240].read()
adc6in240 = (a+b+c)/3
print "D_240 reads ", adc6in240," at 6 inches."

move(w,-1.32,0.831,240,pose)
a =  w.dms[300].read()
move(w,-1.32,0.831,240,pose)
b =  w.dms[300].read()
move(w,-1.32,0.831,240,pose)
c =  w.dms[300].read()
adc6in300 = (a+b+c)/3
print "D_300 reads ", adc6in300," at 6 inches."

print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
move(w,-1.0062,0.831,180,pose)
a = w.dms[0].read()
move(w,-1.0062,0.831,180,pose)
b = w.dms[0].read()
move(w,-1.0062,0.831,180,pose)
c = w.dms[0].read()
adc12in000 = (a+b+c)/3
print "D_000 reads ", adc12in000," at 18 inches."

move(w,-1.0062,0.831,120,pose)
a = w.dms[60].read()
move(w,-1.0062,0.831,120,pose)
b = w.dms[60].read()
move(w,-1.0062,0.831,120,pose)
c = w.dms[60].read()
adc12in060 = (a+b+c)/3
print "D_060 reads ", adc12in060," at 18 inches."

move(w,-1.0062,0.831,60,pose)
a = w.dms[120].read()
move(w,-1.0062,0.831,60,pose)
b = w.dms[120].read()
move(w,-1.0062,0.831,60,pose)
c = w.dms[120].read()
adc12in120 = (a+b+c)/3
print "D_120 reads ", adc12in120," at 18 inches."

move(w,-1.0062,0.831,0,pose)
a = w.dms[180].read()
move(w,-1.0062,0.831,0,pose)
b = w.dms[180].read()
move(w,-1.0062,0.831,0,pose)
c = w.dms[180].read()
adc12in180 = (a+b+c)/3
print "D_180 reads ", adc12in180," at 18 inches."

move(w,-1.0062,0.831,300,pose)
a = w.dms[240].read()
move(w,-1.0062,0.831,300,pose)
b = w.dms[240].read()
move(w,-1.0062,0.831,300,pose)
c = w.dms[240].read()
adc12in240 = (a+b+c)/3
print "D_240 reads ", adc12in240," at 18 inches."

move(w,-1.0062,0.831,240,pose)
a = w.dms[300].read()
move(w,-1.0062,0.831,240,pose)
b = w.dms[300].read()
move(w,-1.0062,0.831,240,pose)
c = w.dms[300].read()
adc12in300 = (a+b+c)/3
print "D_300 reads ", adc12in300," at 18  inches."

# Slope, m, formula: y=mx+b
m000 = (adc12in000 - adc6in000)/12.0
m060 = (adc12in060 - adc6in060)/12.0
m120 = (adc12in120 - adc6in120)/12.0
m180 = (adc12in180 - adc6in180)/12.0
m240 = (adc12in240 - adc6in240)/12.0
m300 = (adc12in300 - adc6in300)/12.0

# Y-intercept, b: y=mx+b
b000 = adc6in000 - m000*6.0
b060 = adc6in060 - m060*6.0
b120 = adc6in120 - m120*6.0
b180 = adc6in180 - m180*6.0
b240 = adc6in240 - m240*6.0
b300 = adc6in300 - m300*6.0

print
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
print
print w.hostname

print "ADC angle 000, slope: ", m000, " , y intercept: ", b000
print "ADC angle 060, slope: ", m060, " , y intercept: ", b060
print "ADC angle 120, slope: ", m120, " , y intercept: ", b120
print "ADC angle 180, slope: ", m180, " , y intercept: ", b180
print "ADC angle 240, slope: ", m240, " , y intercept: ", b240
print "ADC angle 300, slope: ", m300, " , y intercept: ", b300

w.stop()

