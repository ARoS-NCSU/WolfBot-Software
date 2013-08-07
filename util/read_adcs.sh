#!/bin/bash

name[0]=D240
name[2]=D120
name[6]=D000

for i in 6 2 0; do
  cat /sys/devices/ocp.*/helper.*/AIN${i} > /dev/null
  echo -n ${name[$i]}: 
  cat /sys/devices/ocp.*/helper.*/AIN${i}
done

