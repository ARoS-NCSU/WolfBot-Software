class pwm(object):

  def __init__(self, num):
    self.sysfs = '/sys/class/pwm/pwm' + str(num)
    with open(self.sysfs + '/duty_ns', 'r') as f:
      self.duty = int(f.read())
    with open(self.sysfs + '/period_ns', 'r') as f:
      self.period = int(f.read())
    with open(self.sysfs + '/polarity', 'r') as f:
      self.polarity = int(f.read())

  def set_duty(self, val):
    self.duty = val
    with open(self.sysfs + '/duty_ns', 'w') as f:
      f.write(str(val) + '\n')

  def set_period(self, val):
    self.period = val
    with open(self.sysfs + '/period_ns', 'w') as f:
      f.write(str(val) + '\n')

  def set_polarity(self, val):
    self.polarity = val
    with open(self.sysfs + '/polarity', 'w') as f:
      f.write(str(val) + '\n')

  def start(self):
    with open(self.sysfs + '/run', 'w') as f:
      f.write('1\n')

  def stop(self):
    with open(self.sysfs + '/run', 'w') as f:
      f.write('0\n')

