#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
from pygame.locals import *
import matplotlib.pyplot as plt

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from sensor_msgs.msg import Image

import pygame
from pygame.locals import *
import time
import sys
import os

import cv2
from cv_bridge import CvBridge, CvBridgeError
import datetime
import csv

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../config")
import util_config

INFERENCE_TIME = util_config.Inference_time
DISCRETIZATION = util_config.Discretization_number

class joyconController:
    def __init__(self):
        rospy.init_node('joycon_node', anonymous=True)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.image_sub = rospy.Subscriber('front_camera/image_raw', Image, self.callback)

        pygame.joystick.init()
        self.joystick0 = pygame.joystick.Joystick(0)
        self.joystick0.init()
        self.joystickx = 0
        self.joysticky = 0
        pygame.init()

        self.button_cnt = 0
        self.coff_linearx = 0
        self.coff_angularz = -1

        self.linear_max = 1.6
        self.linear_min = -0.6
        """
        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.twist_pub.publish(twist)
        """
        self.current_button = -1

        self.images = []
        self.command = []
        self.tocsv = []
        self.frame_n = 0


        parent_save_name = os.environ['HOME']+'/Images_from_rosbag/'
        if not os.path.exists(parent_save_name):
            os.makedirs(parent_save_name)
        dat = datetime.datetime.now()
        timestamp = str(dat.year).zfill(4)+'-'+str(dat.month).zfill(2)+'-'+str(dat.day).zfill(2)+'-'+str(dat.hour).zfill(2)+'-'+str(dat.minute).zfill(2)+'-'+str(dat.second).zfill(2)
        outputdir = os.environ['HOME'] + '/Images_from_rosbag/_' + timestamp
        
        # determin directory name to be unique
        cnt = 2
        if os.path.exists(outputdir) == True :
            outputdir = outputdir + '_' + str(cnt)
            while (os.path.exists(outputdir)):
                cnt += 1
                outputdir = outputdir[0:len(outputdir)-2] + '_' + str(cnt)
        self.outputimagedir = outputdir + '/images'
        os.makedirs(outputdir)
        os.makedirs(self.outputimagedir)
        self.outputcsv = outputdir + '/_' + timestamp + '.csv'

    def callback(self, image):
        self.current_img = image

    def callback_org(self):
        
        pressed = self.joystick0.get_button(12)

        #終了処理
        if pressed == 1 :
            pygame.quit()
            with open(self.outputcsv, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(self.tocsv)
            for frame in range(self.frame_n):
                cv2.imwrite(self.tocsv[frame][1], self.images[frame])
            exit()

        left_hol=self.joystick0.get_axis(0)
        left_ver= - self.joystick0.get_axis(1)
        right_hol=self.joystick0.get_axis(2)
        right_ver= - self.joystick0.get_axis(5)
        pygame.event.pump()

        twist = Twist()
        # cmd_velのPublish
        if left_ver < 0 :
            left_ver = 0 
        twist.linear.x  = left_ver  * self.linear_max
        twist.angular.z = right_hol * self.coff_angularz
        print 'linear x:' + str(twist.linear.x) + ', angular z:' + str(twist.angular.z)

        rospy.sleep(INFERENCE_TIME)
        self.twist_pub.publish(twist)

        self.images.append(CvBridge().imgmsg_to_cv2(self.current_img, "bgr8"))
        self.command.append(twist.angular.z)

        standardizationed_command = str(int(twist.angular.z*((DISCRETIZATION-1)/2)+((DISCRETIZATION-1)/2)))

        self.tocsv.append([self.frame_n, self.outputimagedir+"/image"+str(self.frame_n).zfill(5)+".jpg",standardizationed_command ])
        self.frame_n += 1

        if self.button_cnt>=10:
            self.button_cnt = 0

if __name__ == '__main__':
    
    if DISCRETIZATION % 2 != 1:
        print "discretization number should be odd number"
        exit()
    
    try:
        jc = joyconController()
        r=rospy.Rate(10)
        time.sleep(2)
        while not rospy.is_shutdown():
            jc.callback_org()
            r.sleep()
        
    except pygame.error:
        print 'コントローラが見つかりませんでした。'
    except rospy.ROSInterruptException: pass

