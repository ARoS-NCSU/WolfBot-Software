import bbb.pwm as pwm

class Camera(object):

    def __init__(self):
        self.pwm = pwm.pwm(2)
        self.pwm.stop()
        self.tilt = 135

    def __str__(self):
        out = "Camera: tilt = %d" % self.tilt
        return out

    def set_tilt(self, angle): 

        pulse_min = 500000
        pulse_max = 2400000
        pulse_range = pulse_max - pulse_min
        step = pulse_range/180

        pulse = pulse_min + angle*step

        self.pwm.set_duty(pulse)
        self.pwm.start()
        self.tilt = angle


