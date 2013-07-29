#!/bin/sh

dir=$(dirname $0)

$dir/setup_ir_gpios.sh
$dir/setup_motor_gpios.sh
$dir/setup_pwm.sh
$dir/setup_adcs.sh
