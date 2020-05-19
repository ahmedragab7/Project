#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sensor_msgs.msg
import random
import numpy as np
from geometry_msgs.msg import Twist
from itertools import *
from operator import itemgetter

LINX = 0.0 #Always forward linear velocity.
THRESHOLD = 0.5 #THRESHOLD value for laser scan.
PI = 3.14
Kp = 0.05
angz = 0

def LaserScanProcess(data):
    length = len(data.ranges)
    print(data.ranges[360])

def main():
    rospy.init_node('listener', anonymous=True)

    #pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("scan", sensor_msgs.msg.LaserScan , LaserScanProcess)

    rospy.spin()

    

if __name__ == '__main__':
    main()
