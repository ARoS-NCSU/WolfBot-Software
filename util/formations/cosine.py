#!/usr/bin/python
from math import sin, cos, pi

def pose(s, params = [1]):
    r = params[0]
    x = 2*(s-0.5)
    y = r*cos(2*pi*(1-s))
    angle = 0
    return x,y,angle

