import bbb

def load_adc_file(filename):
    vals = []
    with open(filename) as f:
        for line in f.readlines():
            vals.append(float(line.split(',')[1]))
    return vals

class DmsMux(object):
    def __init__(self, mux_config):
        self.adc = bbb.ADC(mux_config['ain'])
        self.gpios = []

        # select lines gpios
        #   config file is high bit to low bit, so reverse them
        for g in reversed(mux_config['select_gpios']):
            self.gpios.append( bbb.GPIO(g) )

        adc_vals = None
        if 'adc_file' in mux_config:
            adc_vals = load_adc_file(mux_config['adc_file'])

        self.sensors = {}
        for sensor_config in mux_config['sensors']:
            name = sensor_config['angle']
            # address reads in as an integer, even if config uses binary
            self.sensors[name] = DmsMuxSensor(self, name, sensor_config, adc_vals)

        self.config = mux_config

    def select(self, address):
        # gpios are from high to low
        mask = 1
        for g in self.gpios:
            #g.set_value( bin(address)[-i] )  # match low bits ot low bits, etc
            g.set_value( address & mask )
            mask<<=1  # shift over to the next higher bit

    # address property??

    def read(self):
        return self.adc.raw()
        
    def read_all(self, mode='raw'):
        #result = {}
        #for s in self.sensors:
        #    result[s.name] = s.read()
        return { name:sensor.read(mode) for name,sensor in self.sensors.items() }
         
# a single sensor from a multiplexed group
class DmsMuxSensor(object):
    def __init__(self, mux, name, config, adc_vals=None):
        self.name = name
        self.mux = mux
        self.config = config
        self.address = config['address']
        self.slope_inches = float(config['slope_inches'])
        self.offset = float(config['offset'])
        self.adc_vals = adc_vals

    def read(self, mode='raw'):
        self.mux.select(self.address)
        if mode == 'inch':
            return self._inches()
        else:
            return self._raw()

    def _raw(self):
        return self.mux.adc.raw()

    def _inches(self):
        if self.adc_vals is not None:
            adc = min( len(self.adc_vals)-1, self.mux.adc.raw() )
            return self.adc_vals[adc]
        else:
            #  inches = (adc - offset) / slope
            return (self.mux.adc.mV - self.offset) / self.slope_inches

