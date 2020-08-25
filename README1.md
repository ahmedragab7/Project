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

