import bbb

class LightSensor(object):
    def __init__(self, sensor_config):
        self.config = sensor_config
        self.adc = bbb.ADC(self.config['ain'])

    def read(self):
        percent = 100 * (self.adc.volts() / self.config['v_max'])
        return percent

