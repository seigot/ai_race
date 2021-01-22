#!/usr/bin/env python
import rospy
import time
from sensor_msgs.msg import Image
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

import cv2
from cv_bridge import CvBridge
import numpy as np

import sys
import csv
import math

Max_steer_angle = float(25)/float(180)*3.1415
twist = Twist()
image = np.zeros((240,320,3))
bridge = CvBridge()

def sub_image(data):
    global image
    global bridge
    image = bridge.imgmsg_to_cv2(data,"bgr8")

def sub_twist(msg):
    global twist
    twist = msg

    #publish_image_w_arrow(twist.angular.z)

def add_arrow_in_image(cur_image, z_angle):
    
    cv2.arrowedLine(cur_image, (160,240), (int(160-40*math.sin(z_angle)), int(240-40*math.cos(z_angle))), (0, 0, 255), thickness=3)
    #print "test"

def publish_image_w_arrow():
    global arrow_pub
    msg = Image()
    cur_image = image
    if twist.angular.z > Max_steer_angle:
        steer = Max_steer_angle
    elif twist.angular.z < -Max_steer_angle:
        steer = -Max_steer_angle
    else :
        steer = twist.angular.z

    add_arrow_in_image(cur_image, steer)
    msg.header.stamp = rospy.Time.now()
    msg.data = bridge.cv2_to_imgmsg(cur_image.astype(np.uint8),"bgr8")
    arrow_pub.publish(msg.data)


def init_player():
    rospy.init_node('arrow_added_publisher', anonymous=True)
    rospy.Subscriber('/front_camera/image_raw', Image, sub_image)
    rospy.Subscriber("/cmd_vel", Twist, sub_twist)
    global arrow_pub
    arrow_pub = rospy.Publisher('/front_camera_w_arrow/image_raw', Image, queue_size=1)

    r=rospy.Rate(10)
    while not rospy.is_shutdown():
        publish_image_w_arrow()
        r.sleep()
    
if __name__ == '__main__':
    init_player()
