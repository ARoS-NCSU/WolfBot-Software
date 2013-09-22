import bbb.adc as adc

class LightSensor(object):
    def __init__(self, sensor_config):
        self.config = sensor_config
        self.adc = adc.adc(self.config['ain'])

    def read(self):
        percent = 100 * (self.adc.read() / (1000.0*self.config['v_max']))
        return percent

