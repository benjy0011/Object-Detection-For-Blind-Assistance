#!/usr/bin/env python3
import rospy
from std_msgs.msg import String

import sys
sys.path.insert(1, '/home/benjy/od_ws/src/od_pkg')

from speech_model.vosk_ import Vosk

class listen4command:
    def __init__ (self):
        self.vosk = Vosk()
        self.command = ""
        
        # topic name: command
        self.pub_command = rospy.Publisher('command', String, queue_size=10)
        
        self.loop_rate = rospy.Rate(30)
        
    def listen(self):
        speech = self.vosk.listen() 
        return speech       
            
    def publish(self):
        rospy.loginfo("Publishing command")
        
        while not rospy.is_shutdown() and "exit" not in self.command:
            self.command = ""
            self.command = self.listen()            
            if self.command != "":
                print(f"'{self.command}'")
            self.pub_command.publish(self.command)
            self.loop_rate.sleep()
                         
        rospy.signal_shutdown(print("Exiting"))
        
if __name__ == "__main__":
    rospy.init_node('Vosk', anonymous=True)
    l4c = listen4command()
    l4c.publish()