# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import sys
import tty
import termios

#import keyboard

import time

class Keyboard_Controller:
    def __init__(self):
        rospy.init_node('key_teleop_node', anonymous=True)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1000)
        rospy.Timer(rospy.Duration(0.01), self.timerCallback)
        '''
        # ジョイコン操作用
        pygame.joystick.init()
        self.joystick0 = pygame.joystick.Joystick(0)
        self.joystick0.init()
        pygame.init()
        '''
        self.joystickx = 0
        self.joysticky = 1

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
        """
        print ()
        print ('ジョイコンのLに対応')
        print ('スティックが左になるように横向きに持つ')
        print ('スティック左右でステアリング、▶ボタンで前進、▼ボタンで後退、離すと停止')
        print
        """ 

    def timerCallback(self, event):
        
        twist = Twist()
        key = chr(ord(self.getch()))
        print key
        # イベント処理
        
        if key =="q":
            exit()
        if key == "":
            self.current_button = -1
            # スティックの処理
        elif key == "a" :
            self.button_cnt += 1
            self.current_button = 5
        elif key =="d":
            self.button_cnt += 1
            self.current_button = 6
    # ボタンの処理
        if key =="j":
            self.button_cnt += 1
            self.current_button = 2
        elif key =="l":
            self.button_cnt += 1
            self.current_button = 1
        elif key =="m":
            self.button_cnt += 1
            self.current_button = 0
        elif key =="i":
            self.button_cnt += 1
            self.current_button = 3
        

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
            if self.coff_linearx > self.linear_min :
                self.coff_linearx -= 0.2
            else :
                self.coff_linearx = self.linear_min
            print 
        elif self.current_button==0:
            if self.coff_linearx > 0 :
                self.coff_linearx -= 0.2
            else :
                self.coff_linearx = 0
            print 
        elif self.current_button==1:
            print 
            if self.coff_linearx < self.linear_max :
                self.coff_linearx += 0.2
            else :
                self.coff_linearx = self.linear_max
        elif self.current_button==5:
            if self.coff_angularz > -0.5:
                self.coff_angularz -= 0.2
            else :
                self.coff_angularz = -0.5
        elif self.current_button==6:
            if self.coff_angularz < 0.5 :
                self.coff_angularz += 0.2
            else :
                self.coff_angularz = 0.5
        # cmd_velのPublish
        twist.linear.x  = self.coff_linearx
        twist.angular.z = -self.joysticky * self.coff_angularz
        print 'linear x:' + str(self.coff_linearx) + ', angular z:' + str(self.coff_angularz)
        self.twist_pub.publish(twist)

        if self.button_cnt>=10:
            """
            print 
            print 'ジョイコンのLに対応'
            print 'スティックが左になるように横向きに持つ'
            print 'スティック左右でステアリング、▶ボタンで前進、▼ボタンで後退、離すと停止'
            print
            """ 
            self.button_cnt = 0
            
    def getch(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

if __name__ == '__main__':
    try:
        jc = Keyboard_Controller()
        rospy.spin()
    except pygame.error:
        print 'joystickが見つかりませんでした。'
    except rospy.ROSInterruptException: pass