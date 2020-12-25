#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import csv

import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../config")
import util_config

INFERENCE_TIME = util_config.Inference_time

class keyboardController:
    def __init__(self):
        #ノード初期設定、10fpsのタイマー付きパブリッシャー
        rospy.init_node('keyboard_con_node', anonymous=True)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.image_sub = rospy.Subscriber('front_camera/image_raw', Image, self.callback)
        
        #ボタン関係の初期化
        self.current_button = -1
        self.joystickx = 0
        self.joysticky = 0

        # ボタンのカウントと速度の係数
        self.button_cnt = 0
        self.coff_linearx = 0
        self.coff_angularz = 1

        #MAX値設定
        self.linear_max = 1.6
        self.linear_min = -0.6

        twist = Twist()
        twist.linear.x = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = 0.0
        self.twist_pub.publish(twist)
        
        self.images = []
        self.command = []
        self.tocsv = []
        self.frame_n = 0
        # pygameに初期化
        pygame.init()
        pgscreen=pygame.display.set_mode((1, 1))
        pygame.display.set_caption('keyboardcon')

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
 

        #コントロール方法表示
        print 
        print 'キーボード操作用'
        print 'Aで左、Dで右にステアリング、Lで前進、Mで後退、離すと停止'
        print 


    def callback(self, image):
        self.current_img = image
    
    def callback_org(self):
        print rospy.Time.now()
        global INFERENCE_TIME

        #メッセージ初期化
        twist = Twist()
        
        # イベント処理
        pygame.event.pump()
        pressed = pygame.key.get_pressed()

        #押下の有無判断用カウンタ
        cnt = 0

        #終了処理
        if pressed[K_ESCAPE] :
            pygame.quit()
            with open(self.outputcsv, 'w') as f:
                writer = csv.writer(f)
                writer.writerows(self.tocsv)
            for frame in range(self.frame_n):
                cv2.imwrite(self.tocsv[frame][1], self.images[frame])
            exit()

        #ステアリング検出
        if pressed[K_a] :
            self.joystickx -= 1
            cnt += 1
            self.button_cnt += 1
            if self.joystickx < -1:
                self.joystickx = -1
        if pressed[K_d] :
            self.joystickx += 1
            cnt += 1
            self.button_cnt += 1
            if self.joystickx > 1:
                self.joystickx = 1
        if cnt == 0:
            self.joystickx = 0
        cnt = 0

        #アクセル、バック検出
        if pressed[K_l] :
            self.current_button = 1
            cnt += 1
            self.button_cnt += 1
        if pressed[K_m] :
            self.current_button = 0
            cnt += 1
            self.button_cnt += 1
        if cnt == 0:
            self.current_button = -1
        cnt = 0

        # 実際の値変更
        #   未入力時の処理
        if self.current_button == -1:
            if abs(self.coff_linearx) < 0.1 :
                self.coff_linearx = 0
            if self.coff_linearx > 0 :
                self.coff_linearx -= 0.2
            elif self.coff_linearx < 0 :
                self.coff_linearx += 0.2
            else :
                self.coff_linearx = 0
        
        #   ボタン入力時の処理
        if self.current_button==2:
            print 
        elif self.current_button==3:
            print 
        elif self.current_button==0:
            if self.coff_linearx > self.linear_min :
                self.coff_linearx -= 0.2
            else :
                self.coff_linearx = self.linear_min
            print 0
        elif self.current_button==1:
            print 1
            if self.coff_linearx < self.linear_max :
                self.coff_linearx += 0.2
            else :
                self.coff_linearx = self.linear_max

        # cmd_velのPublish
        twist.linear.x  = self.coff_linearx
        twist.angular.z = -self.joystickx * self.coff_angularz
        print rospy.Time.now()
        print 'linear x:' + str(self.coff_linearx) + ', angular z:' + str(self.joystickx)

        rospy.sleep(INFERENCE_TIME)
        self.twist_pub.publish(twist)

        self.images.append(CvBridge().imgmsg_to_cv2(self.current_img, "bgr8"))
        self.command.append(twist.angular.z)

        self.tocsv.append([self.frame_n, self.outputimagedir+"/image"+str(self.frame_n).zfill(5)+".jpg",twist.angular.z+1 ])
        self.frame_n += 1

        if self.button_cnt>=10:
            print 
            print 'キーボード操作用'
            print 'Aで左、Dで右にステアリング、Lで前進、Mで後退、離すと停止'
            print 
            self.button_cnt = 0

if __name__ == '__main__':
    try:
        kc = keyboardController()
        r=rospy.Rate(10)
        while not rospy.is_shutdown():
            kc.callback_org()
            r.sleep()
        
    except pygame.error:
        print 'コントローラが見つかりませんでした。'
    except rospy.ROSInterruptException: pass
