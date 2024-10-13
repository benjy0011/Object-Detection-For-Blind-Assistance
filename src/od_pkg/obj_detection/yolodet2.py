#!/usr/bin/env python3
import rospy
import ros_numpy
from sensor_msgs.msg import Image
from std_msgs.msg import Float64MultiArray, String

import torch
import numpy as np
import cv2
import yaml
from torchvision import transforms

import os
import sys
sys.path.insert(1, '/home/benjy/od_ws/src/od_pkg')

from utils.datasets import letterbox
from utils.general import non_max_suppression_mask_conf

from detectron2.modeling.poolers import ROIPooler
from detectron2.structures import Boxes
from detectron2.utils.memory import retry_if_cuda_oom
from detectron2.layers import paste_masks_in_image

import time
from math import *

from position import POSITION

import warnings
warnings.filterwarnings('ignore')

# from captioning.captioningOFA import OFA
# from captioning.captioning import LAVIS

class YoloDet2:
    def __init__(self):
        self.intr = None
        self.rgb = None
        self.depth = None
        self.command = ""   
        
        # sys.stdout.write('\rLoading model ......')
        print('\rLoading model ......')
        # setting up device (GPU or else CPU)
        torch.cuda.empty_cache()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Load model from torch
        with open(os.path.expanduser('~')+'/od_ws/src/od_pkg/obj_detection/data/hyp.scratch.mask.yaml') as f:
        # with open('data/hyp.scratch.mask.yaml') as f:
            self.hyp = yaml.load(f, Loader=yaml.FullLoader)
        weigths = torch.load(os.path.expanduser('~')+'/od_ws/src/od_pkg/obj_detection/yolo_weight/yolov7-mask.pt')
        # weigths = torch.load('yolo_weight/yolov7-mask.pt')
        self.model = weigths['model']
        self.model = self.model.half().to(self.device)
        _ = self.model.eval()

        # Names of classes (total 80 from pretrained model)
        self.names = self.model.names
        
        print('\rDone\n')
        
        # Threshold value for confidence score
        self.threshold = 0.5
        
        # Load OFA captioning
        # self.ofa = OFA()
        # self.lavis = LAVIS()
        
        # ROS related        
        self.loop_rate = rospy.Rate(30)
        
        # topic name: Image        
        self.pub_speech = rospy.Publisher('speech', String, queue_size=10)
        
        # topic name: command2
        self.pub_command2 = rospy.Publisher('command2', String, queue_size=10)
        
        rospy.Subscriber('rgb_frame', Image, self.rgb_callback)
        rospy.Subscriber('depth_frame', Image, self.depth_callback)
        rospy.Subscriber('intr', Float64MultiArray, self.intr_callback) 
        rospy.Subscriber('command', String, self.command_callback) 
    
    ''' 
    Preprocessing 
    ''' 
    def image_process(self, image):
        # # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)    
        image = letterbox(image, 640, stride=64, auto=True)[0]
        image = cv2.resize(image, (640,480), interpolation= cv2.INTER_AREA)
        image_ = image.copy()
        image = transforms.ToTensor()(image)
        image = torch.tensor(np.array([image.numpy()]))
        image = image.to(self.device)
        image = image.half()
        output = self.model(image)

        inf_out, train_out, attn, mask_iou, bases, sem_output = output['test'], output['bbox_and_cls'], output['attn'], output['mask_iou'], output['bases'], output['sem']
        
        bases = torch.cat([bases, sem_output], dim=1)
        nb, _, height, width = image.shape
        
        pooler_scale = self.model.pooler_scale
        pooler = ROIPooler(output_size=self.hyp['mask_resolution'], scales=(pooler_scale,), sampling_ratio=1, pooler_type='ROIAlignV2', canonical_level=2)
        
        output, output_mask, output_mask_score, output_ac, output_ab = non_max_suppression_mask_conf(inf_out, attn, bases, pooler, self.hyp, conf_thres=0.25, iou_thres=0.65, merge=False, mask_iou=None)
        
        pred, pred_masks = output[0], output_mask[0]
        base = bases[0]

        return image, image_, height, width, pred, pred_masks     
    
    '''
    Object detection process.
    All relevant info were drawn or showed inside the image/frame.
    Calculate the depth of object from the camera. 
    Return labeled frame and approximate depth of the object.  
    '''
    def obj_detection(self, image, depth_frame, height, width, pred, pred_masks, intr):
        detected_obj = []

        # Processing    
        bboxes = Boxes(pred[:, :4])
        original_pred_masks = pred_masks.view(-1, self.hyp['mask_resolution'], self.hyp['mask_resolution'])
        pred_masks = retry_if_cuda_oom(paste_masks_in_image)( original_pred_masks, bboxes, (height, width), threshold=0.5)
        pred_masks_np = pred_masks.detach().cpu().numpy()
        pred_cls = pred[:, 5].detach().cpu().numpy()
        pred_conf = pred[:, 4].detach().cpu().numpy()
        # nimg = image[0].permute(1, 2, 0) * 255
        # nimg = nimg.cpu().numpy().astype(np.uint8)
        # # nimg = cv2.cvtColor(nimg, cv2.COLOR_RGB2BGR)
        nbboxes = bboxes.tensor.detach().cpu().numpy().astype(int)
        # pnimg = nimg.copy()

        # Go through detections one by one 
        for one_mask, bbox, cls, conf in zip(pred_masks_np, nbboxes, pred_cls, pred_conf):
            if conf < self.threshold:
                continue

            x, y, z = self.cal_coordinate(one_mask, depth_frame)

            ''' source: https://drive.google.com/drive/folders/1-FxgYAKfAFJofLZS13B6m7ihtzJrZ4Sz 
                from: yolo.py'''
            theta = 0  # assume camera is not tilting and is always upright  
            xtemp = z * (x - intr[0]) / intr[2]
            ytemp = z * (y - intr[1]) / intr[3]
            ztemp = z

            # xtarget = xtemp - 35 #35 is RGB camera module offset from the center of the realsense
            xtarget = xtemp 
            ytarget = -(ztemp*sin(theta) + ytemp*cos(theta))
            ztarget = ztemp*cos(theta) + ytemp*sin(theta)  
            
            # add_to_list(detected_obj, names[int(cls)], xtarget, ytarget, ztarget)
            detected_obj.append([self.names[int(cls)], xtarget, ytarget, ztarget])

        return detected_obj
    
    ''' 
    To calculate coordinate.
    There are 2 ways to calculate the depth (idea of mine).
    @ Method 1 is to calculate depth for all points of mask, then compute the median/upper quartile,
    it is accurate, but very slow because need a lot of computation.
    @ Method 2 is to calculate the center point of the mask, then compute the depth,
    it is fast, but less accurate.
    Then proceed to coordinate.
    '''
    def cal_coordinate(self, one_mask, depth_frame):
        count = np.count_nonzero(one_mask) 
        center = np.argwhere(one_mask==1).sum(0)/count

        # @ Method 1
        depth_array = []
        for point in np.argwhere(one_mask):
            depth_array.append(depth_frame[point[0],point[1]])
        # depth = median(depth_array)
        depth = np.percentile(depth_array, 75)

        # # @ Method 2     
        # depth = depth_frame[round(center[0]), round(center[1])]  

        # Get coordinate
        coordinate = [round(center[1]), round(center[0]), depth]       

        return coordinate
    
    '''
    Simple function to calculate steps required in a given distance D.
    Unit in mm.
    Assume one step is around 400mm
    '''
    def cal_steps(self, D):
        return (round((abs(D)/400),1))
    
    ''' 
    A simple function to display time required 
    '''
    def display_time(self, start_time):    
        end_time = time.time()
        total_time = (end_time-start_time)
        print(f'Time: {total_time:.2f} seconds')
    
    def intr_callback(self, data):
        self.intr = data.data     
    
    def rgb_callback(self, data):
        self.rgb = ros_numpy.numpify(data)
    
    def depth_callback(self, data):
        self.depth = ros_numpy.numpify(data)
        
    def command_callback(self, data):
        self.command = data.data
        if self.command != "":
            print("command: "+ self.command)

    def find_object(self):
        found = 0        
        obj_interest = self.ask_user()
        detected_obj = self.detected_obj
        if obj_interest != "":
            speech = ''
            # describe 3 object nearby in single direction (total 6 direction 上下左右前後)
            clarify = 3
            for i in range(len(detected_obj)):
                if obj_interest == detected_obj[i][0] and obj_interest != "":
                    lateral = []; updown  = []; backforth = []; left_object = []; right_object = []; up_object = []; down_object = []; forth_object = []; back_object = []
                    found += 1
                    x,y,z = detected_obj[i][1:4]

                    # Describe the coordinate in more understandable way
                    if y > 0: ypos = "top"                
                    elif y < 0: ypos = "bottom"                
                    else: ypos = "middle"
                        
                    if x > 0: xpos = "right"                
                    elif x < 0: xpos = "left"               
                    else: xpos = "center"            

                    # if z == 0
                    if z <= 0 or z == 0:
                        position = f"\nIts distance cannot be detected, might be too far/near" if found <= 1 else f"\nThe other one its distance cannot be detected, might be too far/near"

                    # if object is near (within 600mm)
                    elif z <= 600 and z >0:
                        pos = "near to the camera"
                        if abs(y) <=80 and abs(x) <= 100:
                            position = f"\nIt is around center position {pos}" if found <= 1 else f"\nThe other one is around center position {pos}" 
                        elif abs(y) >= 80 and abs(x) <= 100:
                            position = f"\nIt is around {ypos} position {pos}" if found <= 1 else f"\nThe other one is around {ypos} position {pos}" 
                        elif abs(y) <= 80 and abs(x) >= 100:
                            position = f"\nIt is around {xpos} hand side {pos}" if found <= 1 else f"\nThe other one is around {xpos} hand side {pos}"
                        else:
                            position = f"\nIt is around {ypos} {xpos} position {pos}" if found <= 1 else f"\nThe other one is around {ypos} {xpos} position {pos}"
                    
                    # if object is at moderate distance
                    elif z >600 and z <=5000:
                        pos = "of the camera"
                        ypos = ypos if abs(y) >= 150 else "in front"
                        zsteps = self.cal_steps(z); xsteps = self.cal_steps(x)
                        position = f"\nIt is around {zsteps} steps to the front, {xsteps} steps to the {xpos}, and is somewhere {ypos} {pos}, mind your steps" if found <= 1 \
                                else f"\nThe other one is around {zsteps} steps to the front, {xsteps} steps to the {xpos}, and is somewhere {ypos} {pos}, mind your steps"
                    
                    # far distance object
                    else:
                        xpos = xpos if abs(x) >= 150 else ""
                        position = f"\nIt is quite far from the camera, please move slightly forward {xpos} and try again, mind your steps" if found <= 1 \
                                else f"\nThe other one is quite far from the camera, please move slightly forward {xpos} and try again, mind your steps"

                    speech += f'{position}.\n' 
                    
                    if z <= 600:
                        for j in range(len(detected_obj)):                    
                            if detected_obj[j][1:4] != [x,y,z]:             
                                xyz = [dist([detected_obj[j][1]], [x]), dist([detected_obj[j][2]], [y]), dist([detected_obj[j][3]], [z])]
                                max_index = [index for index, item in enumerate(xyz) if item == max(xyz)][0]

                                if max_index == 0: lateral.append([detected_obj[j][1], detected_obj[j][0]])
                                elif max_index == 1: updown.append([detected_obj[j][2], detected_obj[j][0]])
                                elif max_index == 2: backforth.append([detected_obj[j][3], detected_obj[j][0]])

                            
                    elif z >600 and z <=5000:
                        for j in range(len(detected_obj)):                    
                            if detected_obj[j][1:4] != [x,y,z]:
                                if dist([detected_obj[j][1]], [x]) < 500 and dist([detected_obj[j][2]], [y]) < 500 and dist([detected_obj[j][3]], [z]) < 450:
                                    xyz = [dist([detected_obj[j][1]], [x]), dist([detected_obj[j][2]], [y]), dist([detected_obj[j][3]], [z])]
                                    max_index = [index for index, item in enumerate(xyz) if item == max(xyz)][0]

                                    if max_index == 0: lateral.append([detected_obj[j][1], detected_obj[j][0]])
                                    elif max_index == 1: updown.append([detected_obj[j][2], detected_obj[j][0]])
                                    elif max_index == 2: backforth.append([detected_obj[j][3], detected_obj[j][0]])

                    lateral.append([x, detected_obj[i][0]])
                    lateral.sort()
                    lat_pos = -1
                    updown.append([y, detected_obj[i][0]])
                    updown.sort()
                    ud_pos = -1
                    backforth.append([z, detected_obj[i][0]])
                    backforth.sort()
                    bf_pos = -1
                    
                    if len(lateral) > 1:
                        # speech += f'\nThere are {len(lateral)-1} item(s) beside it.\n'
                        for k in range(len(lateral)):
                            if x == lateral[k][0]:
                                lat_pos = k
                                # speech += f'It is {POSITION[k]} item from the left.\n'
                                # speech += f'{POSITION[len(lateral)- (k+1)]} item from the right.\n'


                    if len(updown) > 1:
                        # speech += f'\nThere are {len(updown)-1} item(s) above/below of it.\n'
                        for k in range(len(updown)):
                            if y == updown[k][0]:
                                ud_pos = k
                                # speech += f'It is {POSITION[k]} item from the bottom.\n'
                                # speech += f'{POSITION[len(updown)- (k+1)]} item from the top.\n'


                    if len(backforth) > 1:
                        # speech += f'\nThere are {len(backforth)-1} items in backforth of it.\n'
                        for k in range(len(backforth)):
                            if z == backforth[k][0]:
                                bf_pos = k                                
                                # speech += f'It is {POSITION[k]} item from front.\n'
                                # speech += f'{POSITION[len(backforth)- (k+1)]} item from behind.\n'
                    
                    if lat_pos != -1:
                        if lat_pos > 0:
                            try:
                                for a in range(clarify):
                                    if lat_pos-(a+1) >=0 : left_object.append(lateral[lat_pos-(a+1)][1]) 
                            except IndexError:
                                pass        
                            speech += f"\nTo the LEFT you will see: "
                            for item in left_object:
                                speech += f"{item}, "

                        if lat_pos < len(lateral)-1:
                            try:
                                for a in range(clarify):
                                    right_object.append(lateral[lat_pos+(a+1)][1])
                            except IndexError:
                                pass
                            speech += f"\nTo the RIGHT you will see: "
                            for item in right_object:
                                speech += f"{item}, "

                    if ud_pos != -1:
                        if ud_pos > 0:
                            try:
                                for a in range(clarify):
                                    if ud_pos-(a+1) >=0 : down_object.append(updown[ud_pos-(a+1)][1])
                            except IndexError:
                                pass
                            speech += f"\nTo the BOTTOM you will see: "
                            for item in down_object:
                                speech += f"{item}, "

                        if ud_pos < len(updown)-1:
                            try:
                                for a in range(clarify):
                                    up_object.append(updown[ud_pos+(a+1)][1])
                            except IndexError:
                                pass                    
                            speech += f"\nTo the TOP you will see: "
                            for item in up_object:
                                speech += f"{item}, "

                    if bf_pos != -1:
                        if bf_pos > 0:
                            try:
                                for a in range(clarify):
                                    if bf_pos-(a+1) >=0 : forth_object.append(backforth[bf_pos-(a+1)][1])
                            except IndexError:
                                pass                     
                            speech += f"\nTo the FORTH you will see: "
                            for item in forth_object:
                                speech += f"{item}, "

                        if bf_pos < len(backforth)-1:
                            try:
                                for a in range(clarify):
                                    back_object.append(backforth[bf_pos+(a+1)][1])
                            except IndexError:
                                pass                    
                            speech += f"\nTo the BACK you will see: "
                            for item in back_object:
                                speech += f"{item}, "    

                    speech += f'\n'    

            speech = f'I found {found} {obj_interest} in total.\n{speech}' if found else "I cannot locate it, please try again, or move around a little bit.\n"
            print(speech)

            # voice output
            self.pub_speech.publish(speech)
            # self.speak(speech)
            
    '''
    Prompt user for object in interest
    '''
    def ask_user(self):
        cont_listen = True
        while cont_listen:
            # ask_msg = "Please tell object in interest (say 'STOP' to quit)"     
            ask_msg = "Please tell object in interest"             
            print("\n"+ask_msg)
            self.pub_speech.publish(ask_msg)
            speech = ""
            self.command = ""
            while speech == "":                 
                speech = self.command
            print(f"'{speech}'")
            recognized_obj = [name for name in self.names if name in speech]            
            if "stop" in speech or "exit" in speech:
                if "exit" in speech:
                    rospy.signal_shutdown(print("Exiting")) 
                else:
                    print("Stopping...")
                    self.pub_speech.publish("Stopping......")
                cont_listen=False
            elif len(recognized_obj):
                print(f"\nDo you mean '{recognized_obj[0]}'? (reply 'YES' or 'NO')")
                self.pub_speech.publish(f"Do you mean '{recognized_obj[0]}'? (reply 'YES' or 'NO')")
                confirm = ""
                self.command = ""
                while "yes" not in confirm and "no" not in confirm:                    
                    confirm = self.command
                    if "exit" in confirm:
                        rospy.signal_shutdown(print("Exiting"))
                print(f"'{confirm}'")
                if "yes" in confirm:
                    self.inference()
                    cont_listen = False
                    return recognized_obj[0]
            else:    
                print(f"\n{speech} is not identified object, please try again")
                self.pub_speech.publish(f"{speech} is not identified object, please try again")
                time.sleep(2)        
        return ""
            
    def inference(self):
        start_time = time.time()        
        
        # Preprocess each frame
        image, image_, height, width, pred, pred_masks = self.image_process(self.rgb)
        
        self.detected_obj=[]
        
        # if prediction/detection is none
        if pred is None:
            pass
            
        else:
            self.detected_obj = self.obj_detection(image, self.depth, height, width, pred, pred_masks, self.intr)
        
        self.display_time(start_time)
        torch.cuda.empty_cache()
        
    # def ofa_caption(self):
    #     cv2.imwrite('temp.jpg', self.rgb)
    #     description = self.ofa.do_captioning('temp.jpg')
    #     # description = self.lavis.do_captioning(self.rgb)
    #     print(description)
    #     self.pub_speech.publish(description)        
            
    def run(self):
        time.sleep(2)
        print("Ready")
        self.pub_speech.publish("Ready")
        while not rospy.is_shutdown():                                
            if "search" in self.command or "find" in self.command or "locate" in self.command:
                print("Processing......")
                self.pub_speech.publish("Processing......")                
                # self.inference()
                self.find_object()    
                self.command = ""                        
            
            elif "describe" in self.command or "caption" in self.command:
                print("Processing......")
                self.pub_speech.publish("Processing......")
                self.pub_command2.publish("caption")     
                self.command = ""                          
            
            if "exit" in self.command:
                self.pub_command2.publish("exit")
                rospy.signal_shutdown(print("Exiting")) 
                
            self.loop_rate.sleep()
    
if __name__ == '__main__':
    # node name: rsD435
    rospy.init_node('YoloDet2', anonymous=True)
    od = YoloDet2()
    od.run()