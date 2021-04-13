#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import requests
import json
import time

from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry

JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"

CONES = [
    "cone_A",
    "cone_B",
    "cone_C",
    "cone_D",
    "cone_E",
    "cone_F",
    "cone_G",
]
CAR_LENGTH = 0.4
CAR_WIDTH = 0.2

try:
    CONE_WIDTH = rospy.get_param("/collision_surveillance/cone_width")
except:
    pass

# 一度検出した後に次に検出可能になるまでの時間
# mainに書いているけどクラスに書いた方が自然な気がする
COOL_TIME_SEC = 0.3

#TODO: 引数名を真面目に考える
#降順にして返す、sortでやったほうがよい気がしてきた
def get_sorted_pair(a, b):
    if a > b:
        return a, b
    else:
        return b, a

# 値が範囲内にあるかを判定
def is_in_range(value, minimum, maximum):
    if minimum <= value and value <= maximum:
        return True
    else:
        return False

class CollisionDetector(object):

    def __init__(self, cool_time_sec=0):
        self.cool_time_sec = cool_time_sec
        self.current_time = rospy.Time.now().to_sec()
        self.prev_time_when_collision = self.current_time
        self.get_rosparam()
        self.model_states_subscriber = rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback, queue_size=1)
        self.wheel_robot_tracker_x = 0
        self.wheel_robot_tracker_y = 0
        self.wheel_robot_tracker_dx = 0
        self.wheel_robot_tracker_dy = 0
        rospy.Subscriber('/wheel_robot_tracker', Odometry, self.callback_odom)
        self.data = None
        self.obeject_positions = {}

    def get_rosparam(self):
        self.cone_width = rospy.get_param('~cone_width', default=0.2)
        print("cone_width ")
        print(self.cone_width)
    def callback(self, data):
        # check if all CONE objects are spawn in the world.
        # sometimes CONEs are allocated randomly..
        for object_name in CONES:
            try:
                pos = data.name.index(object_name)
            except ValueError:
                print (object_name + " not found!! waiting to be spawned in the world...")
                return

        print("all cones found!!")
        # save data
        self.data = data
        # unregister, if already unnecessary.
        self.model_states_subscriber.unregister()

    def callback_odom(self, msg):
        self.wheel_robot_tracker_dx = msg.pose.pose.position.x - self.wheel_robot_tracker_x
        self.wheel_robot_tracker_dy = msg.pose.pose.position.y - self.wheel_robot_tracker_y
        self.wheel_robot_tracker_x = msg.pose.pose.position.x
        self.wheel_robot_tracker_y = msg.pose.pose.position.y

    def is_collided_rect_and_rect(
            self,
            rect1_x1, rect1_x2, rect1_y1, rect1_y2,
            rect2_x1, rect2_x2, rect2_y1, rect2_y2):
        rect1_x1, rect1_x2 = get_sorted_pair(rect1_x1, rect1_x2)
        rect1_y1, rect1_y2 = get_sorted_pair(rect1_y1, rect1_y2)
        rect2_x1, rect2_x2 = get_sorted_pair(rect2_x1, rect2_x2)
        rect2_y1, rect2_y2 = get_sorted_pair(rect2_y1, rect2_y2)
        if rect1_x1 > rect2_x1:
            if not is_in_range(rect2_x1, rect1_x2, rect1_x1):
                return False
        else:
            if not is_in_range(rect1_x1, rect2_x2, rect2_x1):
                return False
        if rect1_y1 > rect2_y1:
            if not is_in_range(rect2_y1, rect1_y2, rect1_y1):
                return False
        else:
            if not is_in_range(rect1_y1, rect2_y2, rect2_y1):
                return False
        return True

    def get_position(self, data):
        if data is None:
            return 0, 0
        x = self.wheel_robot_tracker_x
        y = self.wheel_robot_tracker_y
        #print(x,y)
        # 障害物の座標が分かっていないなら取得する
        if len(self.obeject_positions) != len(CONES):
            self.obeject_positions = {}
            for object_name in CONES:
                pos = data.name.index(object_name)
                print(object_name)
                print(data.pose[pos].position.x)
                print(data.pose[pos].position.y)
                self.obeject_positions[object_name] = [
                    data.pose[pos].position.x,
                    data.pose[pos].position.y,
                ]
        return x, y

    # http request
    def httpPostReqToURL(self, url, data):
        res = requests.post(url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res

    def UpdateConeCount(self, name):
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {
            "cone": {
                "name" : name,
                "count" : 1
                }
        }
        res = self.httpPostReqToURL(url, req_data)
        return res
    
    # 障害物判定
    @property
    def collided_object(self):
        self.current_time = rospy.Time.now().to_sec()

        if self.data is None:
            return None

        if abs(self.wheel_robot_tracker_dx)+abs(self.wheel_robot_tracker_dy) < 0.1:
            # stack soon after collision
            if self.current_time - self.prev_time_when_collision < self.cool_time_sec:
                self.prev_time_when_collision = self.current_time
                return None

        if self.current_time - self.prev_time_when_collision < self.cool_time_sec:
            # avoid chattering
            return None
        
        car_x, car_y = self.get_position(self.data)
        for object_name, object_position in self.obeject_positions.items():
            object_x, object_y = object_position
            if self.is_collided_rect_and_rect(
                    car_x + CAR_WIDTH / 2, car_x - CAR_WIDTH / 2,
                    car_y + CAR_LENGTH / 2, car_y - CAR_LENGTH / 2,
                    object_x + self.cone_width / 2, object_x - self.cone_width / 2,
                    object_y + self.cone_width / 2, object_y - self.cone_width / 2
                    ):
                self.prev_time_when_collision = self.current_time
                # update Count request
                self.UpdateConeCount(object_name)
                return object_name
        return None

if __name__ == '__main__':
    try:
        rospy.init_node('collision_surveillance', anonymous=True)
        collision_detector = CollisionDetector(COOL_TIME_SEC)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            collided_object = collision_detector.collided_object
            if collided_object is not None:
                print("collided: {}".format(collided_object))
            else:
                pass
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
