import bbb.adc as adc
import bbb.gpio as gpio

class DmsMux(object):
    def __init__(self, mux_config):
        self.adc = adc.adc(mux_config['ain'])
        self.gpios = []

        # select lines gpios
        #   config file is high bit to low bit, so reverse them
        for g in reversed(mux_config['select_gpios']):
            self.gpios.append( gpio.gpio(g) )

        self.sensors = {}
        for sensor_config in mux_config['sensors']:
            name = sensor_config['angle']
            # address reads in as an integer, even if config uses binary
            self.sensors[name] = DmsMuxSensor(self, name, sensor_config)

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
        return self.adc.read()
        
    def read_all(self, mode='raw'):
        #result = {}
        #for s in self.sensors:
        #    result[s.name] = s.read()
        return { name:sensor.read(mode) for name,sensor in self.sensors.items() }
         
# a single sensor from a multiplexed group
class DmsMuxSensor(object):
    def __init__(self, mux, name, config):
        self.name = name
        self.mux = mux
        self.config = config
        self.address = config['address']
        self.slope_inches = float(config['slope_inches'])
        self.offset = float(config['offset'])

    def read(self, mode='raw'):
        self.mux.select(self.address)
        if mode == 'inch':
            return self._inches()
        else:
            return self._raw()

    def _raw(self):
        return self.mux.adc.read()

    # offset and slope ser
    #  inches = (adc - offset) / slope
    def _inches(self):
        return (self._raw() - self.offset) / self.slope_inches

