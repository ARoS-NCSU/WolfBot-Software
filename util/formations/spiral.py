#!/usr/bin/python
from math import sin, cos, pi

def pose(s, params = [1,1,0.5]):
    r = params[0]
    f = params[1]
    shift = params[2]	
    x = r*(s+shift)*cos(2*pi*f*(s+shift))
    y = r*(s+shift)*sin(2*pi*f*(s+shift))
    angle = 0
    return x,y,angle

