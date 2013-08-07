#!/bin/bash

M[1]=pwm4
M[2]=pwm3
M[3]=pwm1

D[1]=gpio31
D[2]=gpio60
D[3]=gpio115

pwms=/sys/class/pwm
gpios=/sys/class/gpio

# disable
echo 0 > $gpios/gpio117/value

for i in `seq 1 3`; do 
  echo 0 > $gpios/${D[$i]}/value
  echo 1000000 > $pwms/${M[$i]}/duty_ns
  echo 1 > $pwms/${M[$i]}/run
done

# enable
echo 1 > $gpios/gpio117/value
