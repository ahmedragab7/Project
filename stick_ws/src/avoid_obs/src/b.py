#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sensor_msgs.msg
import random
import numpy as np
from geometry_msgs.msg import Twist
from itertools import *
from operator import itemgetter
from geometry_msgs.msg import Point, Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf.transformations import euler_from_quaternion



x = 0.0
y = 0.0 
theta = 0.0
stop=0
THRESHOLD=0.3
PI=3.14
turn_angle=0.0
def newOdom(msg):
    global x
    global y
    global theta
    global dis_now
    
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    
    AZ = msg.pose.pose.orientation.z
    AX = msg.pose.pose.orientation.x
    AY =msg.pose.pose.orientation.y
    AW =msg.pose.pose.orientation.w
    orientation_list=[AX,AY,AZ,AW]
    (roll,pitch,theta)=euler_from_quaternion(orientation_list)
     






def LaserScanProcess(data):
    global turn_angle
    scan=data.ranges
    scan_filter=scan[540:719]+scan[0:180]
    
    
    range_angels = np.arange(len(scan_filter))
    ranges = np.array(scan_filter)
    range_mask = (ranges > THRESHOLD)
    
    print("ennnd\n")
    for j in range(1,len(range_mask)-1):
        
        if ((range_mask[j]==False) and (range_mask[j-1]==True) and (range_mask[j+1]==True)):
            range_mask[j]=True
    
    ranges = list(range_angels[range_mask])
    #print(ranges)
    gap_list=[]
    for k, g in groupby(enumerate(ranges), lambda (i,x):i-x):
        gap_list.append(map(itemgetter(1), g))
    
    gap_list.sort(key=len)
    largest_gap = gap_list[-1]
    
    min_angle, max_angle = largest_gap[0]*((data.angle_increment)*180/PI), largest_gap[-1]*((data.angle_increment)*180/PI)
    average_gap = (max_angle - min_angle)/2
    
    #print((average_gap-180)/2)
    turn_angle = min_angle + average_gap
    print(turn_angle)
    turn_angle=turn_angle-90
    turn_angle=(turn_angle*3.14)/180
def main():
    while not rospy.is_shutdown():
        goal_angel=turn_angle+theta
        rospy.init_node('listener', anonymous=True)

    #pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber("scan", sensor_msgs.msg.LaserScan , LaserScanProcess)
        pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
        sub = rospy.Subscriber("/robot_pose_ekf/odom_combined", PoseWithCovarianceStamped, newOdom)
        speed = Twist()
        rospy.spin()
        r = rospy.Rate(4)
        if ((abs(goal_angel - theta) > 0.2) and stop==0):
            rospy.loginfo( "in angular")
            if (goal_angel - theta) > 0:
                speed.linear.x = 0.0
                speed.angular.z = 1.0
            #rospy.loginfo( "in wrong")
            else:
                speed.linear.x = 0.0
                speed.angular.z = -1.0
                rospy.loginfo( "in right") 
        else:
        #rospy.loginfo( "in distance")
            stop=1
        
        
       
        pub.publish(speed)
        r.sleep()    
if __name__ == '__main__':
    main()

