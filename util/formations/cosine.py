#!/usr/bin/python
from math import sin, cos, pi

def pose(s, params = [0.5,1]):
    r = params[0]
    f = params[1]
    x = 2*(s-0.5)
    y = r*cos(2*pi*f*(1-s))
    angle = 0
    return x,y,angle

