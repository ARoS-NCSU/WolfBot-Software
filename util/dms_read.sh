#!/bin/bash

gpios=/sys/class/gpio

A=$gpios/gpio30/value
B=$gpios/gpio3/value
C=$gpios/gpio2/value


for i in "0 0 0" "0 0 1" "0 1 0" "0 1 1" "1 0 0" "1 0 1"; do
    read c b a <<<$(echo $i)
    echo -n "$c$b$a : "
    echo $a > $A
    echo $b > $B
    echo $c > $C
    cat /sys/devices/ocp.*/helper.*/AIN2
done



