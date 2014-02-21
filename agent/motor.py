import bbb

# pwm, dir
motor_cfg = { 1: (4, 31), 
              2: (3, 60),
              3: (1, 115) }

class motor(object):

  def __init__(self, num):
    self.num = num
    self.pwm = bbb.PWM(motor_cfg[num][0])
    self.dir = bbb.GPIO(motor_cfg[num][1])
    self.pwm.stop()
    self.speed = 0

  def __str__(self):
    out = "Motor #%d: Speed = %d, Dir = %d" % (self.num, self.speed, self.dir.get_value())
    return out

  def forward(self): 
    self.dir.set_value(0)
    self.set_speed(self.speed)

  def reverse(self): 
    self.dir.set_value(1)
    self.set_speed(self.speed)

  # TODO: change to a property
  def set_speed(self, speed): 

    duty = int(self.pwm.period * (speed/100.0))

    # need to figure out if we can do thi with polarity instead
    if self.dir.get_value() == 1:
      duty = self.pwm.period - duty
    self.pwm.set_duty(duty)
    self.pwm.start()
    self.speed = speed

  def stop(self): 
    self.set_speed(0)

