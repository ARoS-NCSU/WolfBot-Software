import bbb

class Battery(object):
    def __init__(self, battery_config):
        self.config = battery_config
        self.adc = bbb.ADC(self.config['ain'])
        self.ratio = self.config['ratio']

    def voltage(self):
        # adcs are 12-bit, but report a millivolt value via SysFS
	n = 20
	samples = [ self.adc.volts for i in range(n) ]
        average =  (sum(samples) / n)
        return average / self.ratio

