#!/usr/bin/env python  
import roslib
#roslib.load_manifest('learning_tf')
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf
#import turtlesim.msg
from tf.transformations import euler_from_quaternion

def handle_turtle_pose(msg, turtlename):
    AZ = msg.pose.pose.orientation.z
    AX = msg.pose.pose.orientation.x
    AY =msg.pose.pose.orientation.y
    AW =msg.pose.pose.orientation.w
    orientation_list=[AX,AY,AZ,AW]
    (roll,pitch,theta)=euler_from_quaternion(orientation_list)
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.pose.pose.position.x, msg.pose.pose.position.y, 0),
                     tf.transformations.quaternion_from_euler(0, 0,theta),
                     rospy.Time.now(),
                     turtlename,
                     "world")

if __name__ == '__main__':
    rospy.init_node('turtle_tf_broadcaster')
    turtlename = rospy.get_param('~turtle')
    rospy.Subscriber('/robot_pose_ekf/odom_combined',
                     PoseWithCovarianceStamped,
                     handle_turtle_pose,turtlename)
    rospy.spin()

