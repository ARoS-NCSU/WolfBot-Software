#!/bin/sh

# ./dms_select H M L  
#
# ./dms_select 0 0 1  (would select 1)
# ./dms_select 1 0 0  (would select 4)

base=/sys/class/gpio

A=$base/gpio30/value
B=$base/gpio3/value
C=$base/gpio2/value

echo $3 > $A
echo $2 > $B
echo $1 > $C
