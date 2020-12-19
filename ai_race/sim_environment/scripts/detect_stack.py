#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
import math
import sys

from std_msgs.msg import Float64
from cob_srvs.srv import SetInt, SetIntRequest
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Twist, Pose

class StackDetector:

    def __init__(self):
        self.get_rosparam()
        # rospy.Subscriber("/rear_left_wheel_velocity_controller/command", Float64, self.get_left_command)
        # rospy.Subscriber("/rear_right_wheel_velocity_controller/command", Float64, self.get_right_command)
        rospy.Subscriber("/cmd_vel", Twist, self.get_target_command)
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.get_speed)
        self.respown_srv = rospy.ServiceProxy("/jugemu_new/respown", SetInt)
        self.right_command = 0.0
        self.left_command = 0.0
        self.target_command = 0.0
        self.pre_robot_pos = Pose()
        self.robot_speed = Twist()
        self.pre_t = 0.0
        self.stack_counter = 0.0
        self.pose = Pose()
        
    def get_rosparam(self):
        self.respown_point = rospy.get_param("/respown_point")

    def get_target_command(self, cmd):
        self.target_command = cmd.linear.x

    # def get_left_command(self, msg):
    #     self.left_command = msg.data

    # def get_right_command(self, msg):
    #     self.right_command = msg.data

    def get_speed(self, models):
        try:
            index = models.name.index("wheel_robot")
            self.pose = models.pose[index]
        except ValueError:
            #print ('can not get model.name.index, skip !!')
            pass
        

    def search_nearest_respown(self):
        min_distance = 100.0
        res_num = 0
        res_point = []
        n = 0
        for point in self.respown_point:
            dx = point[0] - self.pose.position.x
            dy = point[1] - self.pose.position.y
            distance = math.sqrt(dx**2 + dy**2)
            if min_distance > distance:
                res_num = n
                min_distance = distance
            n +=1
        res_point = self.respown_point[res_num]
        return res_point, res_num


    def compare_command_value(self):
        # print rospy.Time.now().to_sec(), self.pre_t
        dt = rospy.Time.now().to_sec() - self.pre_t
        if dt <= sys.float_info.epsilon:
            return

        self.robot_speed.linear.x = (self.pose.position.x - self.pre_robot_pos.position.x)/dt
        self.robot_speed.linear.y = (self.pose.position.y - self.pre_robot_pos.position.y)/dt
       
        speed = math.sqrt((self.robot_speed.linear.x)**2 + (self.robot_speed.linear.y)**2)
        # print speed, self.target_command
        if (self.target_command - speed) > 1.0:
            self.stack_counter += 1

        if self.stack_counter > 5:        
            res_point, n = self.search_nearest_respown()
            req = SetIntRequest()
            req.data = int(n)
            print self.respown_srv.call(req)
            self.stack_counter = 0
        
        self.pre_robot_pos = self.pose
        self.pre_t = rospy.Time.now().to_sec()


    def start(self):
        rospy.init_node("detect_stack")
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.compare_command_value()
            rate.sleep()

def main():
    node = StackDetector()
    node.start()

if __name__ == "__main__":
    main()

