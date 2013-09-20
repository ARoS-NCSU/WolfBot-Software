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
            self.sensors[name] = DmsMuxSensor(self, name, sensor_config['address'])

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
        
    def read_all(self):
        #result = {}
        #for s in self.sensors:
        #    result[s.name] = s.read()
        return { name:sensor.read() for name,sensor in self.sensors.items() }
         
# a single sensor from a multiplexed group
class DmsMuxSensor(object):
    def __init__(self, mux, name, address):
        self.name = name
        self.address = address 
        self.mux = mux

    def read(self):
        self.mux.select(self.address)
        return self.mux.adc.read()


# single dms sensor, directly connected (old wolfbots only)
class Dms(object):
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
