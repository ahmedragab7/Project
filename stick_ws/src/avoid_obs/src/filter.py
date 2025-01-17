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
THRESHOLD = 0.3 #THRESHOLD value for laser scan.
PI = 3.14
Kp = 0.05
angz = 0

def LaserScanProcess(data):
    range_angels = np.arange(len(data.ranges))
    ranges = np.array(data.ranges)
    range_mask = (ranges > THRESHOLD)
    ranges = list(range_angels[range_mask])

    #print(ranges)

    max_gap = 40
    # print(ranges)
    gap_list = []
    for k, g in groupby(enumerate(ranges), lambda (i,x):i-x):
        gap_list.append(map(itemgetter(1), g))
    gap_list.sort(key=len)
    largest_gap = gap_list[-1]
    print(largest_gap)
    min_angle, max_angle = largest_gap[0]*((data.angle_increment)*180/PI), largest_gap[-1]*((data.angle_increment)*180/PI)
    average_gap = (max_angle - min_angle)/2
    
    turn_angle = min_angle + average_gap
    print(turn_angle)
    #print(min_angle, max_angle)
    #print(largest_gap,max_gap,average_gap,turn_angle)

    global LINX
    global angz
    if average_gap < max_gap:
        angz = -0.5
    else:
        LINX = 0.5
        angz = Kp*(-1)*(90 - turn_angle)

def main():
    rospy.init_node('listener', anonymous=True)

    #pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber("scan", sensor_msgs.msg.LaserScan , LaserScanProcess)

    rospy.spin()

    

if __name__ == '__main__':
    main()
