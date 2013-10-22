#!/bin/bash

min_pulse=500000
max_pulse=2400000

((range=$max_pulse-$min_pulse))
((step=$range/180))
((pulse=$min_pulse+$1*$step))
echo $pulse > /sys/class/pwm/pwm2/duty_ns
echo 1 > /sys/class/pwm/pwm2/run
