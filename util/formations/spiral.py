#!/usr/bin/python
from math import sin, cos, pi

def pose(s, params = [1,1]):
    r = params[0]
    f = params[1]
    x = r*s*cos(2*pi*f*(s))
    y = r*s*sin(2*pi*f*(s))
    angle = 0
    return x,y,angle

