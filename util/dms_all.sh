#!/bin/bash

gpios=/sys/class/gpio

A=$gpios/gpio30/value
B=$gpios/gpio3/value
C=$gpios/gpio2/value


for i in "000 0 0 0" "060 0 0 1" "120 0 1 0" "180 0 1 1" "240 1 0 0" "300 1 0 1"; do
    read angle c b a <<<$(echo $i)
    echo -n "$c$b$a ($angle) : "
    echo $a > $A
    echo $b > $B
    echo $c > $C
    #cat /sys/devices/ocp.*/helper.*/AIN2
    cat /sys/bus/iio/devices/iio:device0/in_voltage2_raw
done



