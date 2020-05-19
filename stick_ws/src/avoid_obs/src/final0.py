#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from geometry_msgs.msg import PoseWithCovarianceStamped
from math import atan2, sqrt, pow
from sensor_msgs.msg import Imu
from itertools import *
from operator import itemgetter
import sensor_msgs.msg
import numpy as np

x = 0.0
y = 0.0 
theta = 0.0
stop=0
dis_now=0.0
PI=3.14
turn_angle=0.0
THRESHOLD=0.5
trust=11
def LaserScanProcess(data):
    global stop
    global turn_angle
    global trust
    scan=data.ranges
    scan_filter=scan[540:719]+scan[0:180]
    
    counter=0 
    for i in range(len(scan_filter)):
        if(scan_filter[i]<0.3):
            counter+=1
        
    if (counter>130):
        print("danger")
        trust=0
        stop=0
    else:
        print("save")
        stop=4
       
    range_angels = np.arange(len(scan_filter))
    ranges = np.array(scan_filter)
    range_mask = (ranges > THRESHOLD)
    
    
    for j in range(1,len(range_mask)-1):
        
        if ((range_mask[j]==False) and (range_mask[j-1]==True) and (range_mask[j+1]==True)):
            range_mask[j]=True
    
    ranges = list(range_angels[range_mask])
    #print(ranges)
    gap_list=[]
    for k, g in groupby(enumerate(ranges), lambda (i,x):i-x):
        gap_list.append(map(itemgetter(1), g))
    #print("gap_list")
    #print(gap_list)  
    for index in range(len(gap_list)-20):

        if (abs(gap_list[index][-1]-gap_list[index+1][0])<=20):
            range_mask[gap_list[index][-1]+1]=True
            range_mask[gap_list[index][-1]+2]=True
            range_mask[gap_list[index][-1]+3]=True
            range_mask[gap_list[index][-1]+4]=True
            range_mask[gap_list[index][-1]+5]=True
            range_mask[gap_list[index][-1]+6]=True
            range_mask[gap_list[index][-1]+7]=True
            range_mask[gap_list[index][-1]+8]=True
            range_mask[gap_list[index][-1]+9]=True
            range_mask[gap_list[index][-1]+10]=True
            range_mask[gap_list[index][-1]+11]=True
            range_mask[gap_list[index][-1]+12]=True
            range_mask[gap_list[index][-1]+13]=True
            range_mask[gap_list[index][-1]+14]=True
            range_mask[gap_list[index][-1]+15]=True
            range_mask[gap_list[index][-1]+16]=True
            range_mask[gap_list[index][-1]+17]=True
            range_mask[gap_list[index][-1]+18]=True
            range_mask[gap_list[index][-1]+19]=True
            range_mask[gap_list[index][-1]+20]=True


    ranges = list(range_angels[range_mask])
    gap_list_final=[]
    for k, g in groupby(enumerate(ranges), lambda (i,x):i-x):
        gap_list_final.append(map(itemgetter(1), g))

    #print("final:") 
    #print(gap_list_final)
    gap_list_final.sort(key=len)
    
    largest_gap = gap_list_final[-1]
    #print("larg:")
    #print(largest_gap)
    min_angle, max_angle = largest_gap[0]*((data.angle_increment)*180/PI), largest_gap[-1]*((data.angle_increment)*180/PI)
    average_gap = (max_angle - min_angle)/2
    
    #print((average_gap-180)/2)
    turn_angle = min_angle + average_gap
    
    turn_angle=turn_angle-90
    turn_angle=(turn_angle*3.14)/180
    #print("turn_angle:")
    #print(turn_angle)




def newOdom(msg):
    global x
    global y
    global theta
    global dis_now
    
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    dis_now=sqrt(pow(x,2)+pow(y,2))
    AZ = msg.pose.pose.orientation.z
    AX = msg.pose.pose.orientation.x
    AY =msg.pose.pose.orientation.y
    AW =msg.pose.pose.orientation.w
    orientation_list=[AX,AY,AZ,AW]
    (roll,pitch,theta)=euler_from_quaternion(orientation_list)
    #rospy.loginfo("the main is %f",theta) 
rospy.init_node("speed_controller")
sub1=rospy.Subscriber("scan", sensor_msgs.msg.LaserScan , LaserScanProcess)
sub = rospy.Subscriber("/robot_pose_ekf/odom_combined", PoseWithCovarianceStamped, newOdom)

pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)
 
speed = Twist()
 
r = rospy.Rate(4)
 


while not rospy.is_shutdown():
    goal_angel=turn_angle+theta
    
    
    #angle_to_goal=angle_to_goal/3.14
    print(goal_angel)
    print("th:")
    print(theta)
    if ((abs(goal_angel - theta) > 0.21) and (stop<2)  ):
        print( "in angular")
        if (goal_angel - theta) > 0:
            speed.linear.x = 0.0
            speed.angular.z = 1.0
            #rospy.loginfo( "in wrong")
        else:
            speed.linear.x = 0.0
            speed.angular.z = -1.0
            #rospy.loginfo( "in right") 
    
    else:

        if (trust<5):
           
            speed.linear.x = 0.6
            speed.angular.z = 0.0
            trust+=1
          
        else:
           
            speed.angular.z = 0.0
	    speed.linear.x = 0.0



        
        stop+=1
        speed.angular.z = 0.0
     
    pub.publish(speed)
    r.sleep()    


