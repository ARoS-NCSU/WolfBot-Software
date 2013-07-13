#!/bin/sh

#9.12  GPIO1[28] = gpio60   Motor2_Dir
#9.13  GPIO0[31] = gpio31   Motor1_Dir
#9.25  GPIO3[21] = gpio117  Motor_Enable
#9.27  GPIO3[19] = gpio115  Motor3_Dir

sysfs=/sys/class/gpio

for gpio in 31 60 115 117
do
  echo $gpio > ${sysfs}/export
  echo out > ${sysfs}/gpio${gpio}/direction
  echo 0 > ${sysfs}/gpio${gpio}/value
done

