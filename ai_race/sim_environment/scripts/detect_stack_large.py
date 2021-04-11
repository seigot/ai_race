#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
import math
import sys

from std_msgs.msg import Float64
from cob_srvs.srv import SetInt, SetIntRequest
from gazebo_msgs.srv import SetModelState, SetModelStateRequest, SetModelStateResponse
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import Twist, Pose

CONES = [
    "cone_A",
    "cone_B",
    "cone_C",
    "cone_D",
    "cone_E",
    "cone_F",
    "cone_G",
]

class StackDetector:

    def __init__(self):
        self.get_rosparam()
        # rospy.Subscriber("/rear_left_wheel_velocity_controller/command", Float64, self.get_left_command)
        # rospy.Subscriber("/rear_right_wheel_velocity_controller/command", Float64, self.get_right_command)
        rospy.Subscriber("/cmd_vel", Twist, self.get_target_command)
        self.cone_sub = rospy.Subscriber("/gazebo/model_states", ModelStates, self.cone_pos)
        self.cones = []

        self.pose_sub = rospy.Subscriber('/wheel_robot_tracker', Odometry, self.callback_odom)
        self.respown_srv = rospy.ServiceProxy("/jugemu_new/teleport", SetModelState)
        self.right_command = 0.0
        self.left_command = 0.0
        self.target_command = 0.0
        self.pre_robot_pos = Pose()
        self.robot_speed = Twist()
        self.pre_t = 0.0
        self.stack_counter = 0.0
        self.pose = Pose()
        self.odom_theta = 1.57
        
    def get_rosparam(self):
        self.respown_point = rospy.get_param("/respown_point")

    def get_target_command(self, cmd):
        self.target_command = cmd.linear.x

    # def get_left_command(self, msg):
    #     self.left_command = msg.data

    # def get_right_command(self, msg):
    #     self.right_command = msg.data

    def cone_pos(self, models):
        if len(models.name) < 20:
            return

        for object_name in CONES:
            try:
                pos = models.name.index(object_name)
                self.cones.append(models.pose[pos])
            except ValueError:
                print (object_name + " not found!! skip save data...")
                self.cones = []
                return
            


    def callback_odom(self, msg):
        self.pose = msg.pose.pose
        qx = msg.pose.pose.orientation.x
        qy = msg.pose.pose.orientation.y
        qz = msg.pose.pose.orientation.z
        qw = msg.pose.pose.orientation.w
        q = (qx, qy, qz, qw)
        e = tf.transformations.euler_from_quaternion(q)
        self.odom_theta = e[2]

    def search_nearest_respown(self):
        if self.cones == []:
            return self.pose
        min_distance = 100.0
        res_num = 0
        n = 0
        for point in self.cones:
            dx = point.position.x - self.pose.position.x
            dy = point.position.y - self.pose.position.y
            distance = math.sqrt(dx**2 + dy**2)
            if min_distance > distance:
                res_num = n
                min_distance = distance
            n +=1
        return self.cones[res_num]


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
            res_point = self.search_nearest_respown()
            req = SetModelStateRequest()
            if abs(res_point.position.x) >= 2 and abs(res_point.position.y) >= 4:
                center_x = res_point.position.x/abs(res_point.position.x)*2
                center_y = res_point.position.y/abs(res_point.position.y)*4
                dx = res_point.position.x - center_x
                dy = res_point.position.y - center_y
                r = math.sqrt(dx**2 + dy**2)
                theta = math.atan2(dy, dx)
                theta = theta + 10*math.pi/180
                respown_x = r*math.cos(theta) + center_x
                respown_y = r*math.sin(theta) + center_y
                respown_yaw = theta + math.pi/2
                print center_x, center_y, r
                print  respown_x,respown_y, theta
            elif res_point.position.x > 0 and abs(res_point.position.y) < 4:
                respown_x = res_point.position.x
                respown_y = res_point.position.y + 0.5
                respown_yaw = math.pi/2
            elif res_point.position.x < 0 and abs(res_point.position.y) < 4:
                respown_x = res_point.position.x
                respown_y = res_point.position.y - 0.5
                respown_yaw = -math.pi/2
            elif abs(res_point.position.x < 2) and res_point.position.y > 0:
                respown_x = res_point.position.x - 0.5
                respown_y = res_point.position.y
                respown_yaw = math.pi
            elif abs(res_point.position.x < 2) and res_point.position.y < 0:
                respown_x = res_point.position.x + 0.5
                respown_y = res_point.position.y
                respown_yaw = 0
            else:
                respown_x = 5.750014
                respown_y = 0
                respown_yaw = math.pi/2
            req.model_state.pose.position.x = respown_x
            req.model_state.pose.position.y = respown_y
            q = tf.transformations.quaternion_from_euler(0, 0, respown_yaw)
            req.model_state.pose.orientation.x  = q[0]
            req.model_state.pose.orientation.y  = q[1]
            req.model_state.pose.orientation.z  = q[2]
            req.model_state.pose.orientation.w  = q[3]
            print (self.respown_srv.call(req))
            rospy.loginfo("call jugemu !!")
            self.stack_counter = 0

        self.pre_robot_pos = self.pose
        self.pre_t = rospy.Time.now().to_sec()


    def start(self):
        rospy.init_node("detect_stack")
        rate = rospy.Rate(1)
        self.unregistered = False
        while not rospy.is_shutdown():
            self.compare_command_value()
            if self.cones != [] and self.unregistered == False:
                self.cone_sub.unregister()
                self.unregistered = True
                rospy.loginfo("got cone data")
            rate.sleep()

def main():
    node = StackDetector()
    node.start()

if __name__ == "__main__":
    main()

