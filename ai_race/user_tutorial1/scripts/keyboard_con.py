# -*- coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

import sys
import tty
import termios
import select


import time

class TimeoutOccurred(Exception):
    pass

class Keyboard_Controller:
    def __init__(self):
        rospy.init_node('key_teleop_node', anonymous=True)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1000)
        rospy.Timer(rospy.Duration(0.1), self.timerCallback)
        

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
        print 'Lで前進、一回押すとスタート'
        print 'M長押しで停止'
        print 'ステアリングはAで左、Dで右'
        print '複数同時押しには未対応'
        print

    def timerCallback(self, event):
        
        twist = Twist()
        try:
            keys = self.unix_input_with_timeout()
                
            # イベント処理
            for key in keys:
                print "input:" + key
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
            
        except TimeoutOccurred:
            print "timeout"
            self.current_button = -1
        #print key

        # 実際の値変更
        #   未入力時の処理
        if self.current_button == -1:
            self.coff_angularz = 0        

        #   ボタン入力時の処理
        if self.current_button==2:
            print 
        elif self.current_button==3:
            print 
        elif self.current_button==0:
            self.coff_linearx = 0
        elif self.current_button==1:
            self.coff_linearx = 1.6
        elif self.current_button==5:
            self.coff_angularz = -1
        elif self.current_button==6:
            self.coff_angularz = 1
        
        # cmd_velのPublish
        twist.linear.x  = self.coff_linearx
        twist.angular.z = -1 * self.coff_angularz
        print 'linear x:' + str(self.coff_linearx) + ', angular z:' + str(self.coff_angularz)
        self.twist_pub.publish(twist)

        if self.button_cnt>=10:
            
            print 
            print 'Lで前進、一回押すとスタート'
            print 'M長押しで停止'
            print 'ステアリングはAで左、Dで右'
            print '複数同時押しには未対応'
            print
             
            self.button_cnt = 0
            
    def unix_input_with_timeout(self, prompt='', timeout=0.1):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        new = termios.tcgetattr(fd)
        new[3] = new[3] & ~termios.ECHO          # lflags

        termios.tcsetattr(fd, termios.TCSANOW, new)
        tty.setraw(fd)
        (ready, _, _) = select.select([sys.stdin], [], [], timeout)
        if ready:
            termios.tcsetattr(fd, termios.TCSANOW, old)
            return sys.stdin.read(1)
        else:
            termios.tcsetattr(fd, termios.TCSANOW, old)
            raise TimeoutOccurred


if __name__ == '__main__':
    try:
        jc = Keyboard_Controller()
        rospy.spin()
    except pygame.error:
        print 'joystickが見つかりませんでした。'
    except rospy.ROSInterruptException: pass