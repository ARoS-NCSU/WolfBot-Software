import logging
import yaml
from socket import gethostname

class wolfbot(object):

  def __init__(self, config = None):

    self.hostname = gethostname()
    self.load_config(config)
    self.setup_logging()
    self.log.info("Initialized '%s' using config '%s'" % (self.hostname, self.config['config']) )

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
        with open('config/wolfbot.cfg', 'r') as f:
          config = yaml.load(f)
          config['config'] = f.name
      except IOError:
        config = {}
      try:
        with open('config/' + self.hostname + '.cfg', 'r') as f:
          config.update(yaml.load(f))
          config['config'] = f.name
      except IOError:
        pass
    self.config = config

