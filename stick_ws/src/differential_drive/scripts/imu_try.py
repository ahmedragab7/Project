#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Imu
AX=0
AY=0
AZ=0
GX=0
GY=0
GZ=0	
def callback(imu):
    global AX,AY,AZ,GX,GY,GZ
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    AX = int(imu.data[imu.data.index("A")+1:imu.data.index("B")])
    AY = int(imu.data[imu.data.index("B")+1:imu.data.index("C")])
    AZ = int(imu.data[imu.data.index("C")+1:imu.data.index("D")])
    GX = int(imu.data[imu.data.index("D")+1:imu.data.index("E")])
    GY = int(imu.data[imu.data.index("E")+1:imu.data.index("F")])
    GZ = int(imu.data[imu.data.index("F")+1:imu.data.index("G")])


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("imu", String, callback)
    

    # spin() simply keeps python from exiting until this node is stopped
   



def talker():
    global AX,AY,AZ,GX,GY,GZ
    pub = rospy.Publisher('imu_data', Imu, queue_size=100)
    imu=Imu()
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        now = rospy.Time.now()
               
        imu.header.stamp = now
        imu.header.frame_id = "mpu_frame"
        
        imu.linear_acceleration_covariance[0] = 0.0;
        imu.linear_acceleration_covariance[4] = 0.0;
        imu.linear_acceleration_covariance[8] = 0.0;

        imu.angular_velocity_covariance[0] = 0.0;
        imu.angular_velocity_covariance[4] = 0.0;
        imu.angular_velocity_covariance[8] = 0.0;

        imu.orientation_covariance[0] = 0.0;
        imu.orientation_covariance[4] = 0.0;
        imu.orientation_covariance[8] = 0.0;
        imu.angular_velocity.x = GX;
        imu.angular_velocity.y = GY;
        imu.angular_velocity.z = GZ;

        imu.linear_acceleration.x = AX;
        imu.linear_acceleration.y = AY;
        imu.linear_acceleration.z = AZ;





        pub.publish(imu)
        rate.sleep()



if __name__ == '__main__':
    listener()
    talker()
