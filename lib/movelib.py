#!/usr/bin/python

"""
Movement library.

Move to specified pose based on feedback from a localization function that
provides global pose information.

"""

import sys
sys.path.append('/wolfbot/agent')
sys.path.append('/wolfbot/lib')
import logging
import argparse

import time
from math import atan2,pi,degrees,radians, sin,cos,sqrt


def interpolate_sensor(angle, sensors):
    log = logging.getLogger(__name__)

    angle = normalize(angle) % 360
    sens_angles = sensors.keys()
    # find sensors on either side:
    span = 60

    def nearest(angle):
        return (int(round(angle/60.0))*60) % 360

    left = nearest(angle + 30)
    right = nearest(angle - 30)
    log.debug("Normed: %0.2f, Left: %d, right: %d", angle, left, right)
    log.debug("Sensors: %s", [ "%d: %0.2f" % (a,sensors[a]) for a in sorted(sensors)])
    w_l = 1-(left - angle)/60
    w_r = 1-(angle-right)/60
    val = w_l * sensors[left] + w_r * sensors[right]
    log.debug("Val: %0.2f (w_l: %0.2f, w_r: %0.2f)", val, w_l, w_r)

    return val


def normalize(angle):
    """ return angle in [-180,180] """
    rad = radians(angle)
    nor_rad = atan2(sin(rad),cos(rad))
    deg = degrees(nor_rad)
    return deg


def sensor_vector(sensors, minval = 4.0, invert=True):
    x_tot = 0.0
    y_tot = 0.0
    for angle, val in sensors.items():
        # cutoff due to minimum useful sensor distance
        # TODO: add minval as a property of the dms sensor class
        if val < minval:
            val = minval
        if invert:
            val = 1.0/val
        x = val * cos(radians(angle))
        y = val * sin(radians(angle))
        x_tot += x
        y_tot += y

    scale = 100 / (2*1.0/minval)
    mag = scale * sqrt(x_tot**2 + y_tot**2)
    angle = degrees(atan2(y_tot, x_tot)) % 360

    return angle, mag

def add_vectors( vec1, vec2 ):
    """ vecs are ang, mag """
    x1 = vec1[1] * cos(radians(vec1[0]))
    y1 = vec1[1] * sin(radians(vec1[0]))
    x2 = vec2[1] * cos(radians(vec2[0]))
    y2 = vec2[1] * sin(radians(vec2[0]))
    mag = sqrt((x1+x2)**2 + (y1+y2)**2)
    angle = degrees(atan2(y1+y2, x1+x2)) % 360
    return angle, mag


# globals for goto =(
_to_z = _to_x = _to_theta = None
tot_err_dist = tot_err_theta = 0

def goto(wb, to_z, to_x, to_theta, localizer):

    log = logging.getLogger(__name__)

    k_p = 1000.0
    k_i = 50
    #k_i = 100  # oscillates
    #kr_p = 1  # this is suprisingly good for just p!
    kr_p = 1  # this is suprisingly good for just p!
    kr_i = 0.2

    global _to_z, _to_x, _to_theta
    global tot_err_dist, tot_err_theta
    # ugly global to catch target changes across calls
    # FIXME: separate settng target from goto, clear integrators when target set
    if not ((to_z == _to_z) and (to_x == _to_x) and (to_theta == _to_theta)):
        log.info("New target detected, resetting integrators")
        tot_err_dist = tot_err_theta = 0.0
        _to_z = to_z
        _to_x = to_x
        _to_theta = to_theta

    pose = localizer()
    log.info("Pose: %0.3f, x: %0.3f @ %0.1f" % (pose['z'],pose['x'],pose['yaw']))

    log.info("Moving to z: %0.2f, x: %0.2f @ %0.1f" % (to_z,to_x,to_theta))
    err_z = to_z - pose['z']
    err_x = to_x - pose['x']
    err_theta = normalize(to_theta - pose['yaw'])
    dist_to_goal = sqrt(err_x**2 + err_z**2)

    if abs(dist_to_goal) < 0.1:  # only accum when close
        tot_err_dist += dist_to_goal  # never goes down?
    log.debug("Dist to goal %0.2f" % dist_to_goal)

    #if abs(tot_err_theta * kr_i) < 100:   # clamp to useful maximum
    if abs(err_theta) < 25:  # only accum when close
        tot_err_theta += err_theta
    log.debug("Integrators: dist: %0.2f, theta: %0.2f" % (tot_err_dist,tot_err_theta))

    ang_to_goal = degrees(atan2(err_x,err_z))
    rel_to_goal = ang_to_goal - pose['yaw']
    log.info("Relative angle to goal: %0.2f" % rel_to_goal)

    move_speed = k_p * dist_to_goal + k_i*tot_err_dist
    move_speed = min(100,move_speed)

    rotation = kr_p * err_theta + kr_i*tot_err_theta
    rotation = max(-100,min(100,rotation))

    log.info("Goal-only params: %0.1f @ %0.1f deg, %0.1f rotation" %
            (move_speed, rel_to_goal, rotation))

    all_sensors = wb.dms_mux.read_all(mode='inch') # use inch since calibrated
    log.debug("Sensors: %s", [ "%d: %0.2f"%(k,all_sensors[k]) for k in sorted(all_sensors.keys()) ] )
    obs_ang, obs_mag = sensor_vector(all_sensors)
    log.debug("Sensor vector is: %0.2f @ %0.1f deg", obs_mag, obs_ang)

    # neg obs_mag to move away
    combo_ang, combo_mag = add_vectors( (rel_to_goal, move_speed), (obs_ang, -3*obs_mag) )
    log.debug("Combined vector is: %0.2f @ %0.1f deg", combo_mag, combo_ang)
    combo_mag = min(100,combo_mag)


    if False:
        left90 = rel_to_goal + 90
        right90 = rel_to_goal - 90
        left_val = interpolate_sensor(left90,all_sensors)
        right_val = interpolate_sensor(right90,all_sensors)

    # end here and combine with avoidance in a parent function?
    #wb.move_rotate(rel_to_goal,rotation,move_speed=move_speed)

    wb.move_rotate(combo_ang,rotation,move_speed=combo_mag)

    return err_z, err_x, err_theta

def goto_and_stop(wb, z, x, theta, get_pose, precision = 0.03):
    log = logging.getLogger(__name__)
    e_trans = 999
    e_theta = 999
    while (e_trans > precision) or (abs(e_theta) > precision*50):
        log.debug("========================")
        #e_z, e_x, e_theta = goto( wb, args.z, args.x, args.theta, fakepose)
        e_z, e_x, e_theta = goto( wb, z, x, theta, get_pose)
        e_trans = sqrt(e_z**2 + e_x**2)
        log.debug("Error to goal - Translation: %0.3f (%0.3f, %0.3f), Rotation: %0.2f" %
                (e_trans, e_z, e_x, e_theta))
    wb.stop()

def fakepose():
    return {'z':1.01, 'x':0.01, 'yaw':0.0}

if __name__ == '__main__':

    def cleanup(signum, frame):
        wb.stop()
        sys.exit()

    import wolfbot
    import optitrack
    import signal

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    parser = argparse.ArgumentParser()
    parser.add_argument('z', type=float, default=0.0)
    parser.add_argument('x', type=float, default=0.0)
    parser.add_argument('theta', type=float, default=0.0)
    parser.add_argument('-p' , '--precision', type=float, default=0.03)
    parser.add_argument('-d' , '--debug', action='store_true', default=False)
    args = parser.parse_args()

    LOG_FORMAT = '%(asctime)s %(name)s | %(levelname)s | %(message)s'
    if args.debug:
        logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
    else:
        logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
    log = logging.getLogger(__name__)
    log.info('Startup!')

    wb = wolfbot.wolfbot()
    wb.log.setLevel(logging.INFO)
    #wb.log.setLevel(logging.DEBUG)
    opti = optitrack.Optitrack()

    goto_and_stop(wb,args.z,args.x,args.theta,opti.get_pose)

    log.info('Done!')

