#!/bin/sh

sysfs=/sys/class/gpio

# NSEW IR reciever inputs
for gpio in 86 87 88 89
do
  echo $gpio > ${sysfs}/export
  echo in > ${sysfs}/gpio${gpio}/direction
done

# IR receiver enable
echo 49 > ${sysfs}/export
echo out > ${sysfs}/gpio49/direction
echo 0 > ${sysfs}/gpio49/value
