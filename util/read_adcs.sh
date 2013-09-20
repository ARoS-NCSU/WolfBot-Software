#!/bin/bash

name[0]=---
name[1]=---
name[2]=DMS
name[3]=---
name[4]=---
name[5]=---
name[6]=BAT

for i in `seq 0 6`; do
  #cat /sys/devices/ocp.*/helper.*/AIN${i} > /dev/null
  echo -n "$i : ${name[$i]} : "
  cat /sys/devices/ocp.*/helper.*/AIN${i}
done

