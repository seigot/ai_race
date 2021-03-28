#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy

from gazebo_msgs.msg import ModelStates


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
CONE_WIDTH = 0.2

# 一度検出した後に次に検出可能になるまでの時間
# mainに書いているけどクラスに書いた方が自然な気がする
COOL_TIME = 30

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

    def __init__(self, cool_time=0):
        self.cool_time = cool_time
        self.cool_time_left = 0
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.callback, queue_size=1)
        self.data = None
        self.obeject_positions = {}

    def callback(self, data):
        self.data = data
        self.cool_time_left -= 1

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
        try:
            pos = data.name.index('wheel_robot')
        except ValueError:
            return 0, 0
        x = data.pose[pos].position.x
        y = data.pose[pos].position.y
        # 障害物の座標が分かっていないなら取得する
        if len(self.obeject_positions) != len(CONES):
            self.obeject_positions = {}
            for object_name in CONES:
                pos = data.name.index(object_name)
                self.obeject_positions[object_name] = [
                    data.pose[pos].position.x,
                    data.pose[pos].position.y,
                ]
        return x, y

    # 障害物判定
    @property
    def collided_object(self):
        if self.data is None or self.cool_time_left > 0:
            return None
        car_x, car_y = self.get_position(self.data)
        for object_name, object_position in self.obeject_positions.items():
            object_x, object_y = object_position
            if self.is_collided_rect_and_rect(
                    car_x + CAR_WIDTH / 2, car_x - CAR_WIDTH / 2,
                    car_y + CAR_LENGTH / 2, car_y - CAR_LENGTH / 2,
                    object_x + CONE_WIDTH / 2, object_x - CONE_WIDTH / 2,
                    object_y + CONE_WIDTH / 2, object_y - CONE_WIDTH / 2
                    ):
                self.cool_time_left = self.cool_time
                return object_name
        return None

if __name__ == '__main__':
    try:
        cool_time = 0
        rospy.init_node('collision_surveillance', anonymous=True)
        collision_detector = CollisionDetector(COOL_TIME)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            collided_object = collision_detector.collided_object
            if collided_object is not None:
                print("collided: {}".format(collided_object))
            else:
                print("not collided")
                pass
    except rospy.ROSInterruptException:
        pass
