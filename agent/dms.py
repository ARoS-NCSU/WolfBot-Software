import bbb.adc as adc

# TODO: cache last read and only refresh after reasonable delay

class dms(object):
  def __init__(self, dms_config):
    self.adc = adc.adc(dms_config['ain'])
    self.config = dms_config
    self.angle = int(dms_config['angle'])

  def raw(self):
    return self.adc.read()

  def dist(self):
    slope = float(self.config['slope'])
    offset = float(self.config['offset'])
    return  self.raw() * slope + offset

  def contact(self):
    if self.adc.read() > self.config['contact']:
      return True
    return False

  def status(self):
    val = self.adc.read()
    if val > self.config['contact']:
      state = 'contact'
    else:
      state = 'normal'
    return (val, state)
