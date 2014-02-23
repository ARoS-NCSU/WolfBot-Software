#!/usr/bin/python
from math import sin, cos, pi

def pose(s, params = [1]):
    r = params[0]
    x = r*cos(2*pi*(1-s)
    y = r*sin(2*pi*(1-s)
    angle = 0
    return x,y,angle

