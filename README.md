
# Object Detection System For Blind Assistance

This is my internship project, integrating AI models such as YOLOv7 object segmentation, VOSK speech-to-text, OFA image captioning, and a depth camera. This repository is for self-reference purposes, so it has not been fully tidied up. This project won me the **ViTrox Tech4Good Challenge 2023 - 2nd Runner-Up**.

## Brief Description

ROS (Robot Operating System) is required for this project, as it was initially developed for robotics purposes. Additionally, it requires the installation and configuration of certain AI models mentioned below. Some of the necessary files and configurations are included in the folder, with the rest listed below for setup.

## ⭐Features
- Object detection with distance info
- Voice controlled
- Image captioning (describe current frame)

## Additional Info

### Create Workshop
$ mkdir -p ~/od_ws/src  
$ cd ..  
$ catkin_make  
$ source devel/setup.bash  
$ echo $ROS_PACKAGE_PATH  

### ROS Package
$ cd ~/od_ws/src  
$ catkin_create_pkg beginner_tutorials std_msgs rospy roscpp  
$ cd ..  
$ catkin_make  
$ source ~/od_ws/devel/setup.bash  
(move the file into the created pkg)

### To use speech recognition
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
![10](https://github.com/user-attachments/assets/1568197c-5fd6-42ca-91e5-9e173797f60d)
![inference](https://github.com/user-attachments/assets/45df0bbe-5efb-4631-83ff-aba473e58bea)


- Video (notice the detected voice on the right side)  
https://github.com/user-attachments/assets/340fe6c5-3b16-4674-89dc-195a0597e4f7





