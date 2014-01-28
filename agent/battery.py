import bbb.adc as adc

class Battery(object):
    def __init__(self, battery_config):
        self.config = battery_config
        self.adc = adc.adc(self.config['ain'])
        self.ratio = self.config['ratio']

    def voltage(self):
        # adcs are 12-bit, but report a millivolt value via SysFS
	n = 20
	samples = [ self.adc.read() for i in range(n) ]
        average =  (sum(samples) / n)
        return average / (1000.0 * self.ratio)

