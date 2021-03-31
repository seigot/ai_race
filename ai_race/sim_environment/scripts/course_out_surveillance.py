#!/usr/bin/env python
import rospy
import dynamic_reconfigure.client
import time

from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
import requests
import json

#max speed param
MAX_SPEED_W = 0.5

#Track Size Parameters
Lx = rospy.get_param('/course_size_lx', 1.2)
Ly = rospy.get_param('/course_size_ly', 1.04)
r  = rospy.get_param('/course_size_r', 0.75)
Lx_out = rospy.get_param('course_size_lx_out', 2.25)
Ly_out = rospy.get_param('course_size_ly_out', 2.85)

x = 1.6
y = 0.0

dynamic_client = None
curr_max_speed_coeff = 1.0

JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"

#for debug
def print_pose(data):
    pos = data.name.index('wheel_robot')
    print "position:" + '\n' + '\tx:' + str(data.pose[pos].position.x) + '\n' + '\ty:' + str(data.pose[pos].position.y) + '\n' + '\tz:' + str(data.pose[pos].position.z) + '\n' + " orientation:" + '\n' + '\tx:' + str(data.pose[pos].orientation.x) + '\n' + '\ty:' + str(data.pose[pos].orientation.y) + '\n' + '\tz:' + str(data.pose[pos].orientation.z) + '\n' + "\033[8A",

def dynamic_recon_callback(config):
    rospy.loginfo("Config set to {max_speed_coeff}".format(**config))
    global curr_max_speed_coeff
    curr_max_speed_coeff = config.max_speed_coeff

def xy_update(data):
    global x
    global y

    try:
        pos = data.name.index('wheel_robot')
        x = data.pose[pos].position.x
        y = data.pose[pos].position.y
    except ValueError:
        #print ('can not get model.name.index, skip !!')
        pass

def callback_odom(msg):
    global x
    global y
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

def judge_course_l1():
    global dynamic_client
    global x
    global y
    #print data
    #pos = data.name.index('wheel_robot')
    #x = data.pose[pos].position.x
    #y = data.pose[pos].position.y
    #print pos
    #print x
    #print y

    course_out_flag = False

    if abs(x) >= Lx_out or abs(y) >= Ly_out:
        course_out_flag = True
    elif abs(y) <= Ly:
        if abs(x) <= Lx:
            course_out_flag = True
    elif y > Ly:
        if   (abs(x) <  (Lx - r)) and (y < (Ly + r)):
            course_out_flag = True
        elif (x >=  (Lx - r)) and ((x - (Lx - r))**2 + (y - Ly)**2 < r**2):
            course_out_flag = True
        elif (x <= -(Lx - r)) and ((x + (Lx - r))**2 + (y - Ly)**2 < r**2):
            course_out_flag = True
    elif y < -Ly:
        if   (abs(x) <  (Lx - r)) and (y > -(Ly + r)):
            course_out_flag = True
        elif (x >=  (Lx - r)) and ((x - (Lx - r))**2 + (y + Ly)**2 < r**2):
            course_out_flag = True
        elif (x <= -(Lx - r)) and ((x + (Lx - r))**2 + (y + Ly)**2 < r**2):
            course_out_flag = True

    if   (course_out_flag == True)  and (curr_max_speed_coeff != MAX_SPEED_W):
        print "OK -> wwww"
        dynamic_client.update_configuration({"max_speed_coeff":MAX_SPEED_W})
        # courseout count
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {
            "courseout_count": 1
        }
        res = httpPostReqToURL(url, req_data)
    elif (course_out_flag == False) and (curr_max_speed_coeff == MAX_SPEED_W):
        print "wwww -> OK"
        dynamic_client.update_configuration({"max_speed_coeff":1.0})


def course_out_surveillance():
    global dynamic_client
    rospy.init_node('course_out_surveillance', anonymous=True)
    dynamic_client = dynamic_reconfigure.client.Client("dynamic_recon_server_node", timeout=30, config_callback=dynamic_recon_callback)
    #rospy.Subscriber("/gazebo/model_states", ModelStates, xy_update, queue_size = 10)
    rospy.Subscriber('/wheel_robot_tracker', Odometry, callback_odom)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        judge_course_l1()
        rate.sleep()
"""
    # spin() simply keeps python from exiting until this node is stopped
      rospy.spin()
"""

# http request
def httpPostReqToURL(url, data):
    res = requests.post(url,
                        json.dumps(data),
                        headers={'Content-Type': 'application/json'}
    )
    return res

if __name__ == '__main__':
    try:
        course_out_surveillance()
    except rospy.ROSInterruptException:
        pass

