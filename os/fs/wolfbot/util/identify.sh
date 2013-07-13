#!/bin/bash

time=${1:-1}

sysfs=/sys/devices/ocp.2/gpio-leds.?/leds/
name=beaglebone\:green:\usr

save_leds () {
  for i in `seq 0 3`; do
    led[$i]=$(cat ${sysfs}/${name}$i/trigger | awk -F"[\[\]]" '{print $2}')
  done
}

restore_leds () {
  for i in `seq 0 3`; do
    echo ${led[$i]} > ${sysfs}/${name}$i/trigger
  done
}

flash_leds () {
  for i in `seq 0 3`; do
    echo default-on > ${sysfs}/${name}$i/trigger
  done
}

show_leds () {
  for i in `seq 0 3`; do
    echo -n "$i : "
    cat ${sysfs}/${name}$i/trigger | awk -F"[\[\]]" '{print $2}'
  done
}

#show_leds
save_leds
flash_leds
sleep $time
restore_leds
