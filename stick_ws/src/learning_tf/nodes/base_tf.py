#!/usr/bin/env python
import roslib
roslib.load_manifest('learning_tf')
import rospy
import tf


if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    br=tf.TransformBroadcaster()
    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        br.sendTransform((0.0,0.0,0.05),(0.0,0.0,0.0,1.0),rospy.Time.now(),"base_link","base_footprint")
        rate.sleep()

