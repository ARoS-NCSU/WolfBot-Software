#!/bin/sh

rx_en_gpio=/sys/class/gpio/gpio49
tx_pwm=/sys/class/pwm/pwm7

# turn off our receivers
echo 0 > $rx_en_gpio/value

# pulse the pwm (a full 56kHz stream will overheat the LEDs)
/wolfbot/util/pulse.py
