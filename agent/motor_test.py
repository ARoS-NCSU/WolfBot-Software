import gpio
import motor

m1 = motor.motor(1)
m2 = motor.motor(2)
m3 = motor.motor(3)

g = gpio.gpio(117)
g.set_value(1)
