# Robot to guid the blind by ROS 

#inspiration  
Briefly i found that all devices made for the blind are limmited in warning him when he is about to collide , but what if he does't even know where the place that want to go is ? so my project is solving this problem 


# The tasks of the robot :  
1- build a map to the place   
2- navigate throught it (move from place to other )
3- object detection system by tensorflow
4- voice system 
![n](https://user-images.githubusercontent.com/40636325/91198534-f7195100-e6fc-11ea-8346-5269cbf436c3.png)
![n2](https://user-images.githubusercontent.com/40636325/91198542-f8e31480-e6fc-11ea-8492-9a2dcc890c28.png)


# how to use the robot :  

first : you need to build a map by:
1- **roslaunch differential_drive mapping.launch**
2-type in new terminal : **rosrun gmapping slam_gmapping**
3- After finishing the map type :**rosrun map_server map_saver -f <map_name>

then we need to change the name of map in directory :*stick_ws/src/differential_drive/move_base.launch* to the new map name  

now we are ready to navigate in this map :  
1- **roslaunch differential_drive robot.launch**  
2- **roslaunch differential_drive move_base.launch** 
3- **rosrun rviz rviz**
4- choose the initial pose and final pose by : **2D Pose Estimate** and **2D Nave Goal** respectively  

the last thing is object detection :
1- **roslaunch raspicam_node camerav1_1280x720.launch**
2- **rolaunch tensorflow_object_detector_ros object_detection_edited.launch**

# the project video on youtube :https://youtu.be/hQke3YzZzvc  
[![robot to guide the blind by ROS (robotics operating system)](https://img.youtube.com/vi/hQke3YzZzvc/0.jpg)](https://www.youtube.com/watch?v=hQke3YzZzvc)




