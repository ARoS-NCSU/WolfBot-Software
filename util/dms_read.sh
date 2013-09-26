#!/bin/bash

base=/sys/class/gpio

SEL_A_GPIO=$base/gpio30/value  # low
SEL_B_GPIO=$base/gpio3/value   # 
SEL_C_GPIO=$base/gpio2/value   # high

SEL_A=$(cat $SEL_A_GPIO)
SEL_B=$(cat $SEL_B_GPIO)
SEL_C=$(cat $SEL_C_GPIO)

NUM=$(( $SEL_A + 2*$SEL_B + 4*$SEL_C ))

echo -n "DMS ($NUM): "
cat /sys/devices/ocp.*/helper.*/AIN2
