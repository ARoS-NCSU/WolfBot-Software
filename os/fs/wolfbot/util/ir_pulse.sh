#!/bin/bash

pwm=/sys/class/pwm/pwm7

clean_up () {
  echo 0 > $pwm/run
  exit
}

trap clean_up SIGHUP SIGINT SIGTERM

while :; do 
  echo 1 > $pwm/run
  sleep 0.003
  echo 0 > $pwm/run
  sleep 0.01
done


