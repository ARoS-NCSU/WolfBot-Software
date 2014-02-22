import socket
import yaml
from math import degrees,asin,atan2,pi

# http://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToEuler/
# NB: commented version from wikipedia, produces incorrect results?
def euler(quat):
    x,y,z,w = quat

    check = x*y + z*w
    epsilon = 0.001
    # North pole singularity
    #print "Check: ", check
    if( check > 0.5 - epsilon):
        yaw = 2.0 * atan2(x,w);
        pitch = pi/2
        roll = 0
        return degrees(yaw),degrees(pitch),degrees(roll)
    # South pole singularity
    if( check < -0.5 + epsilon):
        yaw = -2.0 * atan2(x,w);
        pitch = -pi/2
        roll = 0
        return degrees(yaw),degrees(pitch),degrees(roll)


    # roll(bank), phi, about x-axis
    #roll = atan2(2*(w*x+y*z),1-2*(x*x+y*y)) 
    roll = atan2(2*(x*w-y*z),1-2*(x*x-z*z)) 

    # pitch(elevation), theta, about y-axis
    #pitch = asin(2*(w*y-x*z))
    pitch = asin(2*(x*y+z*w))

    # yaw(heading), psy, about z-axis
    #yaw = atan2(2*(w*z+x*y),1-2*(y*y+z*z))
    yaw = atan2(2*(y*w-x*z),1-2*(y*y-z*z)) 

    return degrees(yaw),degrees(pitch),degrees(roll)

class Optitrack(object):

    def __init__(self, port=5000):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(0)
        sock.bind(('0.0.0.0', port))
        self.sock = sock
        self.port = port
        self.buffer = 1024


    def get_pose(self):
        """ Read through the receive buffer until we get the latest position
            Returns a dictionary of: {x, y, z, yaw, pitch, roll}
        """
        msg = None
        while True:
            try:
                msg, addr = self.sock.recvfrom(self.buffer)
                #print "got msg"
            except socket.error:
                if not msg:
                    #print "waiting for msg"
                    pass
                else:
                    data = yaml.load(msg)
                    position = data['position']
                    orientation = euler(data['orientation'])
                    x,y,z = position
                    yaw,pitch,roll = orientation
                    if x == y == z == yaw == pitch == roll == 0.00:
                        #print "BAD pose data!"
                        # should we return with an exception/flag or keep trying??
                        # NOTE: tt_streamer now filters these results on its end
                        pass
                    else:
                        return {'x':x, 'y':y, 'z':z, 
                                'yaw':yaw, 'pitch':pitch, 'roll':roll}

    def get_position(self):
        pose = self.get_pose()
        return pose['x'], pose['y'], pose['z']

    def get_orientation(self):
        pose = self.get_pose()
        return pose['yaw'], pose['pitch'], pose['roll']
