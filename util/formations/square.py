#!/usr/bin/python
from math import pi

def pose(s, params = [1.0,1.0,0.0,0.0,0.0]):
        width = params[0]
        height = params[1]
        x_offset = params[2]
        y_offset = params[3]
        rotation = params[4]
        tot_len = 2*(width+height)
        if s <= (width)/(tot_len):
                y = height 
                x = (s*tot_len)
        elif (width)/(tot_len) < s <= (width+height)/tot_len:
                y = (s*tot_len)-width
                x = width
        elif (width+height)/tot_len < s <= (2*width+height)/tot_len:
                y = 0 
                x = (s*tot_len)-width-height 
        elif (2*width+height)/tot_len < s <= 2*(width+height)/tot_len:
                y = (s*tot_len)-width-height-width 
                x = 0
        angle = 0
        x = x + x_offset-(width/2)
        y = y + y_offset-(height/2)
        return x,y,angle
