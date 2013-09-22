import bbb.adc as adc

class Battery(object):
    def __init__(self, battery_config):
        self.config = battery_config
        self.adc = adc.adc(self.config['ain'])
        self.ratio = self.config['ratio']

    def voltage(self):
        # adcs are 12-bit, but report a millivolt value via SysFS
        voltage = (self.adc.read() / 1000.0) / self.ratio
        return voltage

