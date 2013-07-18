#!/bin/bash

slots=/sys/devices/bone_capemgr.*/slots
sysfs=/sys/class/pwm

pwm_to_pin[0]=P9_31  # ehr0A
pwm_to_pin[1]=P9_29  # ehr0B
pwm_to_pin[2]=P9_42  # ecap0
pwm_to_pin[3]=P9_14  # ehr1A
pwm_to_pin[4]=P9_16  # ehr1B
pwm_to_pin[5]=P8_19  # ehr2A
pwm_to_pin[6]=P8_13  # ehr2B
pwm_to_pin[7]=P9_28  # ecap2

load_slot () {
  cat $slots | grep -q $1
  if [ $? -eq 0 ]; then
    echo Module $1 already loaded
  else 
    echo $1 > $slots
  fi
} 

load_pwm () {
  num=$1
  if [ ! -e $sysfs/pwm${num} ]; then
    echo  $num > $sysfs/export
    load_slot bone_pwm_${pwm_to_pin[$num]}
  else
    echo "PWM $num already exported"
  fi
  echo 0 > $sysfs/pwm${num}/run
}

set_duty () {
  echo $2 > $sysfs/pwm${1}/duty_ns
}

set_period () {
  echo $2 > $sysfs/pwm${1}/period_ns
}

set_polarity () {
  echo $2 > $sysfs/pwm${1}/polarity
}

run_pwm () {
  echo 1 > $sysfs/pwm${1}/run
}

load_slot am33xx_pwm

# servo on ecap0
load_pwm 2
set_period 2 10000000
set_duty   2  1924925   # 135 degrees
#set_duty   2  2400000
set_polarity 2 0
run_pwm 2

# IR on ecap2
load_pwm 7
set_period 7 18000
set_duty   7 12000
set_polarity 7 0

# Motor1 on EHRPM1B (pwm4)
load_pwm 4
set_period 4 1000000
set_duty   4  250000
set_polarity 4 0

# Motor2 on EHRPM1A (pwm3)
load_pwm 3
set_period 3 1000000
set_duty   3  250000
set_polarity 3 0

# Motor3 on EHRPM0B (pwm1)
load_pwm 1
set_period 1 1000000
set_duty   1  250000
set_polarity 1 0

