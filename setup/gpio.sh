#!/bin/bash

gpio_sysfs=/sys/class/gpio

load_gpio () {
  num=$1
  if [ ! -e $gpio_sysfs/gpio${num} ]; then
    echo $num > ${gpio_sysfs}/export
  else
    echo "GPIO $num already exported"
  fi
  dir=$2
  if [ "$dir" == "out" ]; then
    echo out > ${gpio_sysfs}/gpio${num}/direction
    echo 0 > ${gpio_sysfs}/gpio${num}/value
  else
    echo in > ${gpio_sysfs}/gpio${num}/direction
  fi
}
