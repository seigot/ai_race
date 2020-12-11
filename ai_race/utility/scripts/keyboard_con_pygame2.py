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
        
        # pygameに初期化
        pygame.init()
        pgscreen=pygame.display.set_mode((1, 1))
        pygame.display.set_caption('keyboardcon')

        #コントロール方法表示
        print 
        print 'キーボード操作用'
        print 'Aで左、Dで右にステアリング、Lで前進、Mで後退、離すと停止'
        print 


    def callback(self, event):
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
            sys.exit()

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

        if self.button_cnt>=10:
            print 
            print 'キーボード操作用'
            print 'Aで左、Dで右にステアリング、Lで前進、Mで後退、離すと停止'
            print 
            self.button_cnt = 0

if __name__ == '__main__':
    try:
        kc = keyboardController()
        rospy.spin()
    except pygame.error:
        print 'コントローラが見つかりませんでした。'
    except rospy.ROSInterruptException: pass
