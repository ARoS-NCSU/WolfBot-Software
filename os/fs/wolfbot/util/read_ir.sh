#!/bin/bash

sysfs=/sys/class/gpio

gpio_N=gpio89
gpio_S=gpio88
gpio_E=gpio87
gpio_W=gpio86

do_values () {
    echo N:$north S:$south E:$east W:$west
}

do_single () {
  if [ $north -eq 0 -a $south -eq 0 -a $west -eq 0 -a $east -eq 0 ]; then 
    echo X
  elif [ $north -eq 0 ]; then 
    echo N
  elif [ $south -eq 0 ]; then 
    echo S
  elif [ $east -eq 0 ]; then
    echo E
  elif [ $west -eq 0 ]; then
    echo W
  else 
    echo X
  fi
}

do_compass () {
    x[0]=+
    x[1]=-
    echo "   ${x[$north]}"
    echo " ${x[$west]} + ${x[$east]}"
    echo "   ${x[$south]}"
}

north=$(cat ${sysfs}/${gpio_N}/value)
south=$(cat ${sysfs}/${gpio_S}/value)
east=$(cat ${sysfs}/${gpio_E}/value)
west=$(cat ${sysfs}/${gpio_W}/value)

case "$1" in 
  values)
    do_values
    ;;
  single)
    do_single
    ;;
  compass)
    do_compass
    ;;
  *)
    do_values
    ;;
esac
