# Object Detection System For Blind Assistance
This is my internship project, it integrated AI models such as YOLOv7 object segmentation, VOSK speech-to-text, OFA image captioning, and a depth camera. This repo is just for self reference purpose so I did not tidy it up. Also, this project won me ViTrox Tech4Good Challenge 2023 - 2nd Runner Up.

## Brief Description
ROS is requried for this project, as initially it was developed for robotics purpose. Also, it requires the installation/configuration of certain AI model as mentioned above and below. Some of the required files and confugurations I have already included in the folder, the rest I listed down below.

## Additional Info 
### Create workshop
$ mkdir -p ~/od_ws/src
$ cd ..
$ catkin_make

$ source devel/setup.bash
$ echo $ROS_PACKAGE_PATH

### package
$ cd ~/od_ws/src
$ catkin_create_pkg beginner_tutorials std_msgs rospy roscpp
$ cd ..
$ catkin_make
$ source ~/od_ws/devel/setup.bash
# move the file into the created pkg

## To use speech recognition
$ pip3 install vosk

### To use captioning
$ cd
$ git clone https://github.com/OFA-Sys/OFA
$ pip install -r requirements.txt

## How to use
$ source ~/od_ws/devel/setup.bash
$ roscore #optional
$ roslaunch od_pkg od.launch


### Hardware
- Intel RealSense Depth Cam
- GPU with 6gb
- A microphone

## Demo
#   O b j e c t - D e t e c t i o n - F o r - B l i n d - A s s i s t a n c e  
 