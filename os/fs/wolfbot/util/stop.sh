#!/bin/bash

M[1]=pwm4
M[2]=pwm3
M[3]=pwm1

pwms=/sys/class/pwm
gpios=/sys/class/gpio

# disable
echo 0 > $gpios/gpio117/value

for i in `seq 1 3`; do 
  echo 0 > $pwms/${M[$i]}/run
done

