import sys
sys.path.append('pybbb')
import logging
import yaml
from math import sin, radians
import motor, lsm, dms
import bbb.gpio as gpio
from socket import gethostname

class wolfbot(object):

  def __init__(self, config = None):

    self.hostname = gethostname()
    self.load_config(config)
    self.setup_logging()
    self.log.info("Initializing '%s' using config '%s'" % (self.hostname, self.config['config']) )

    # TODO: move details into a drive_set(?)
    self.motors = {}
    for i in [1,2,3]:
      self.motors[i] = motor.motor(i)
    self.motor_enable = gpio.gpio(117)

    self.accel = lsm.accel()
    self.mag = lsm.mag()

    self.dms = []
    for dms_cfg in self.config['dms']:
      self.dms.append( dms.dms(dms_cfg) )

    self.log.debug("Initization complete")

  def setup_logging(self):
    logger = logging.getLogger(self.config['name'])
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(module)s %(message)s')
    if(self.config['logfile']):
      fh = logging.FileHandler(self.config['logfile'])
      fh.setFormatter(formatter)
      logger.addHandler(fh) 
    else:
      ch = logging.StreamHandler()
      ch.setFormatter(formatter)
      logger.addHandler(ch) 
    logger.setLevel(logging.DEBUG)
    self.log = logger

  def load_config(self, config = None):
    if config:
      with open(config, 'r') as f:
        config = yaml.load(f)
        config['config'] = f.name
    else:
      try:
        with open('/wolfbot/config/wolfbot.cfg', 'r') as f:
          config = yaml.load(f)
          config['config'] = f.name
      except IOError:
        config = {}
      try:
        with open('/wolfbot/config/' + self.hostname + '.cfg', 'r') as f:
          config.update(yaml.load(f))
          config['config'] = f.name
      except IOError:
        pass
    self.config = config

  def stop(self):
    self.log.info("Stopping motors")
    self.motor_enable.set_value(0)

  def move(self, heading, speed = 100):
    # TODO: 100 isn't max speed in all directions

    self.log.info("Move: %d degrees, speed %d" % (heading, speed))
    vel = {}

    # 0 is straight, Motor 1 is 60, 2 is 180, 3 is 300/-60
    vel[1] = speed * sin(radians(240-heading))
    vel[2] = speed * sin(radians(0-heading))
    vel[3] = speed * sin(radians(120-heading))

    for m,v in vel.items():
      if v > 0:
        self.motors[m].forward()
      else:
        # TODO: Allow set_speed to take negative values(?)
        self.motors[m].reverse()
        v = -v
      self.motors[m].set_speed(v)
      self.log.debug("%s" % self.motors[m])

    self.motor_enable.set_value(1)

  def turn(self, dir, speed = 100):
    if dir == 'cw':
      for i in [1,2,3]:
        self.motors[i].reverse()
        self.motors[i].set_speed(speed)
    if dir == 'ccw':
      for i in [1,2,3]:
        self.motors[i].forward()
        self.motors[i].set_speed(speed)
    self.motor_enable.set_value(1)

