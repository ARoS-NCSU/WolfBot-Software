import pwm
import gpio

# pwm, dir
motor_cfg = { 1: (4, 31), 
              2: (3, 60),
              3: (1, 115) }

class motor(object):

  def __init__(self, num):
     self.pwm = pwm.pwm(motor_cfg[num][0])
     self.dir = gpio.gpio(motor_cfg[num][1])
     self.pwm.stop()
     self.speed = 0

  def forward(self): 
     self.dir.set_value(0)
     self.set_speed(self.speed)

  def reverse(self): 
     self.dir.set_value(1)
     self.set_speed(self.speed)

  # TODO: change to a property
  def set_speed(self, speed): 
     duty = int(self.pwm.period * (speed/100.0))
     if self.dir.get_value() == 1:
       duty = self.pwm.period - duty
     self.pwm.set_duty(duty)
     self.pwm.start()
     self.speed = speed

  def stop(self): 
     self.pwm.stop()

