#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import time

import pyttsx3

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init(driverName='espeak')
        self.speech = []
        self.command = ""
        self.caption = ""
        
        self.loop_rate = rospy.Rate(60)
        rospy.Subscriber('speech', String, self.speech_callback)
        rospy.Subscriber('command', String, self.command_callback)
        
    def speech_callback(self, data):
        s = data.data
        self.speech.append(s.lower())     
        
    def command_callback(self, data):
        self.command = data.data
        
    def caption_callback(self, data):
        self.caption = data.data
        
    def speak_out(self, speech):           
        self.engine.say(speech)
        self.engine.runAndWait()
        self.engine.stop()
    
    def run(self):
        fast = 0; warned=0
        while not rospy.is_shutdown() and "exit" not in self.command:
            if len(self.speech) > 2:
                fast = 1
                
            if not fast and len(self.speech):                 
                self.speak_out(self.speech[0])
                self.speech.pop(0)     
            
            elif fast and len(self.speech):
                if not warned:
                    self.speak_out("You are talking to fast, please wait")
                warned=1                
                self.speak_out(self.speech[-1])
                for i in range (len(self.speech)-1):
                    self.speech.pop(0)
                                       
            self.loop_rate.sleep()
            
        self.speak_out("Exiting")
        rospy.signal_shutdown(print("Exiting"))
            
if __name__ == "__main__":
    # node name: Speaker
    rospy.init_node('Speaker', anonymous=True)
    sp = Speaker()
    sp.run()