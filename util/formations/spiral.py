#!/usr/bin/python
from math import sin, cos, pi

def pose(s, params = [1,1]):
    r = params[0]
    f = params[1]
    x = r*(s-.3)*cos(2*pi*f*(s-.3))
    y = r*(s-.3)*sin(2*pi*f*(s-.3))
    angle = 0
    return x,y,angle

