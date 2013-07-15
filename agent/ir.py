import time

pwm_sys = '/sys/class/pwm/pwm7/'
gpio_sys = '/sys/class/gpio/gpio49/'

def ir_pulse(duration_ms):
  end_time = time.time() + (duration_ms/1000.0)
  rx_off()

  #print "IR pulse active"
  while time.time() < end_time:
    with open(pwm_sys + 'run', 'w') as f:
      f.write('1\n')  
    #sleep(0.001) 
    with open(pwm_sys + 'run', 'w') as f:
      f.write('0\n')  
    time.sleep(0.001)

  #print "IR idle"
  rx_on()

def ir_off():
  with open(pwm_sys + 'run', 'w') as f:
    f.write('0\n')  

def rx_on():
  with open(gpio_sys + 'value', 'w') as f:
    f.write('1\n')

def rx_off():
  with open(gpio_sys + 'value', 'w') as f:
    f.write('0\n')
  
