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

import os
import sys
import csv

args = sys.argv
if len(args) < 2 :
    csvfilename = "/home/jetson/Position_Logs/_2021-01-20-04-15-06/pos.csv"
else :
    csvfilename = args[1]

pos = []
image = np.zeros((480, 640, 3))
image += 255
frame_n = 0
bridge = CvBridge()
start_flag = False
flag_img = cv2.imread(os.path.abspath(__file__)[:-len(os.path.basename(__file__))] + 'flag.jpg')
flag_img = cv2.resize(flag_img,(int(flag_img.shape[1]/2), int(flag_img.shape[0]/2)))

# subscript godeye image
def sub_image(data):
    global image
    global bridge
    image = bridge.imgmsg_to_cv2(data, "bgr8")

# add flag onto godeye image
def add_flag_in_image(image,(x,y)):
    global flag_img
    #make flag figure mask to transcript on godeye vision
    flag_img_mask_tmp = cv2.cvtColor(flag_img, cv2.COLOR_BGR2GRAY)
    th, flag_img_mask_tmp = cv2.threshold(flag_img_mask_tmp, 60, 255, cv2.THRESH_BINARY)
    flag_img_mask = np.zeros((flag_img_mask_tmp.shape[0],flag_img_mask_tmp.shape[1],3))
    flag_img_mask[:,:,0] = flag_img_mask_tmp[:,:]/255
    flag_img_mask[:,:,1] = flag_img_mask_tmp[:,:]/255
    flag_img_mask[:,:,2] = flag_img_mask_tmp[:,:]/255
    flag_img = np.zeros_like(flag_img)
    flag_img[:,:,2] = flag_img_mask_tmp[:,:]
    flag_img_mask = flag_img_mask.astype(np.uint8)

    #or operation between godeye image and flag mask
    #after that, subtract flag figure from godeye image and add flag image to godeye image
    img_cp = image[x:x+flag_img.shape[0],y:y+flag_img.shape[1],:]*(flag_img_mask)
    image[x:x+flag_img.shape[0],y:y+flag_img.shape[1],:] -= img_cp
    image[x:x+flag_img.shape[0],y:y+flag_img.shape[1],:] += flag_img

# publish godeye image with champion flag
def publish_champ_image():
    global image
    global frame_n
    global bridge
    global start_flag

    msg = Image()
    if frame_n < len(pos):
        add_flag_in_image(image,(-int(float(pos[frame_n][0])*70)+240-flag_img.shape[0],-int(float(pos[frame_n][1])*70)+320 ))
    msg.header.stamp = rospy.Time.now()
    msg.data = bridge.cv2_to_imgmsg(image.astype(np.uint8),"bgr8")
    champ_pub.publish(msg.data)
    print frame_n
    if start_flag:
        frame_n+=1

# detect machine start
def time_start(data):
    if data.linear.x != 0 :
        sub_once.unregister()
        global start_flag
        start_flag = True

def init_player():
    rospy.init_node('champion_publisher', anonymous=True)
    rospy.Subscriber('/godeye_camera/image_raw', Image, sub_image)
    global sub_once
    sub_once = rospy.Subscriber("/cmd_vel", Twist, time_start)
    global champ_pub
    champ_pub = rospy.Publisher('/godeye_camera_w_champ/image_raw', Image, queue_size=1)

    global pos
    with open(csvfilename) as f:
        reader = csv.reader(f, delimiter=",")
        pos = [row for row in reader]
    #rospy.spin()

    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        publish_champ_image()
        r.sleep()
if __name__ == '__main__':
    init_player()