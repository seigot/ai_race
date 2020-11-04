# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import pygame
from pygame.locals import *
import time

class joyconController:
    def __init__(self):
        rospy.init_node('joycon_node', anonymous=True)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1000)
        rospy.Timer(rospy.Duration(0.1), self.timerCallback)

        # ジョイコン操作用
        pygame.joystick.init()
        self.joystick0 = pygame.joystick.Joystick(0)
        self.joystick0.init()
        self.joystickx = 0
        self.joysticky = 0
        pygame.init()

        # ボタンのカウントと速度の係数
        self.button_cnt = 0
        self.coff_linearx = 0
        self.coff_angularz = 1

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

        self.current_button = -1

        print 
        print 'ジョイコンのLに対応'
        print 'スティックが左になるように横向きに持つ'
        print 'スティック左右でステアリング、▶ボタンで前進、▼ボタンで後退、離すと停止'
        print 

    def timerCallback(self, event):
        
        twist = Twist()
        eventlist = pygame.event.get()
        # イベント処理
        for e in eventlist:
            print e.type
            if e.type == QUIT:
                return
            # スティックの処理
            if e.type == pygame.locals.JOYHATMOTION:
                self.button_cnt += 1
                self.joysticky, self.joystickx = self.joystick0.get_hat(0) # 横持ち対応のためにxとyを入れ替え
            # ボタンの処理
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                self.button_cnt += 1
                if e.button==2:
                    self.current_button = 2
                elif e.button==1:
                    self.current_button = 1
                elif e.button==0:
                    self.current_button = 0
                elif e.button==3:
                    self.current_button = 3
            elif e.type == pygame.locals.JOYBUTTONUP:
                self.current_button  = -1
        
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
        twist.angular.z = -self.joysticky * self.coff_angularz
        print 'linear x:' + str(self.coff_linearx) + ', angular z:' + str(self.coff_angularz)
        self.twist_pub.publish(twist)

        if self.button_cnt>=10:
            print 
            print 'ジョイコンのLに対応'
            print 'スティックが左になるように横向きに持つ'
            print 'スティック左右でステアリング、▶ボタンで前進、▼ボタンで後退、離すと停止'
            print 
            self.button_cnt = 0

if __name__ == '__main__':
    try:
        jc = joyconController()
        rospy.spin()
    except pygame.error:
        print 'joystickが見つかりませんでした。'
    except rospy.ROSInterruptException: pass