#!/bin/sh

rx_en_gpio=/sys/class/gpio/gpio49
tx_pwm=/sys/class/pwm/pwm7

# turn off our pwm
echo 0 > $tx_pwm/run

# turn on our receivers
echo 1 > $rx_en_gpio/value

