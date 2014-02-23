import sys
import os
import logging
import yaml
from math import sin, radians
import motor, lsm, dms, battery, lightsensor, camera
import bbb
from socket import gethostname

class wolfbot(object):

    def __init__(self, config = None):

        self.hostname = gethostname()
        self.load_config(config)
        self.setup_logging()
        self.log.info("Initializing '%s' using config '%s'" % (self.hostname, self.config['config']) )

        # TODO: move details into a drive_set(?)
        self.motors = {}
        for i in [1,2,3]:
            self.motors[i] = motor.motor(i)
        self.motor_enable = bbb.GPIO(117)

        self.accel = lsm.accel()
        self.mag = lsm.mag()

        self.dms_mux = dms.DmsMux(self.config['dms_mux'])
        self.dms = self.dms_mux.sensors

        self.battery = battery.Battery(self.config['battery'])
        self.lightsensor = lightsensor.LightSensor(self.config['lightsensor'])
        self.camera = camera.Camera()

        self.log.debug("Initization complete")

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
                with open('/wolfbot/config/wolfbot.cfg', 'r') as f:
                    config = yaml.load(f)
                    config['config'] = f.name
            except IOError:
                config = {}
            try:
                with open('/wolfbot/config/' + self.hostname + '.cfg', 'r') as f:
                    config.update(yaml.load(f))
                    config['config'] = f.name
            except IOError:
                pass
        self.config = config

    def stop(self):
        self.log.info("Stopping motors")
        self.motor_enable.set_value(0)

    def move(self, heading, speed = 100):
        # TODO: 100 isn't max speed in all directions

        self.log.info("Move: %d degrees, speed %d" % (heading, speed))
        vel = {}

        # 0 is straight, Motor 1 is 60, 2 is 180, 3 is 300/-60
        vel[1] = speed * sin(radians(240-heading))
        vel[2] = speed * sin(radians(0-heading))
        vel[3] = speed * sin(radians(120-heading))

        for m,v in vel.items():
            if v > 0:
                self.motors[m].forward()
            else:
                # TODO: Allow set_speed to take negative values(?)
                self.motors[m].reverse()
                v = -v
            self.motors[m].set_speed(v)
            self.log.debug("%s" % self.motors[m])

        self.motor_enable.set_value(1)

    def turn(self, dir, speed = 100):
        self.log.warn("Wolfbot.turn() is deprecated, use Wolfbot.rotate()!")
        if dir == 'cw':
            speed = -speed
        self.rotate(speed)

    def rotate(self, speed):
        """ Rotation is CCW for positive speed (i.e., in the +theta direction) """
        if speed < 0:
            speed = abs(speed)
            for i in [1,2,3]:
                self.motors[i].reverse()  # CW
                self.motors[i].set_speed(speed)
        else:
            for i in [1,2,3]:
                self.motors[i].forward()  # CCW
                self.motors[i].set_speed(speed)
        self.motor_enable.set_value(1)

    def move_rotate(self, heading, rotation, move_speed = 50):

        self.log.info("Moving %0.2f degrees @ speed %0.2f, while turning @ %0.2f" %
                (heading, move_speed, rotation))
        vel = {}

        # can't have full turn and full translate simulaneously
        total_speed = move_speed + abs(rotation)
        if total_speed > 100:
            move_speed = 100 * move_speed / total_speed
            rotation = 100 * rotation / total_speed
        self.log.debug("Norm'd speeds - Move: %0.2f, Rotate: %0.2f: ", move_speed, rotation)

        # 0 is straight, Motor 1 is 60, 2 is 180, 3 is 300/-60
        vel[1] = move_speed * sin(radians(240-heading)) + rotation
        vel[2] = move_speed * sin(radians(0-heading)) + rotation
        vel[3] = move_speed * sin(radians(120-heading)) + rotation

        #self.log.debug("Vels %s", vel)

        for m,v in vel.items():
            if v > 0:
                self.motors[m].forward()
            else:
                # TODO: Allow set_speed to take negative values(?)
                self.motors[m].reverse()
                v = -v
            self.log.debug("Setting motor #%d to %0.2f" % (m,v))
            self.motors[m].set_speed(v)

        self.motor_enable.set_value(1)
