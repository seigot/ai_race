#!/usr/bin/env python
import rospy
import dynamic_reconfigure.client
import time
import sys
import os
import datetime

from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Bool
from geometry_msgs.msg import Twist
import requests
import json
import csv


#Level1 Parameters
x = 1.6
y = 0.0
start_time = 0
end_time = 0

dynamic_client = None
curr_max_speed_coeff = 1.0

JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"

parent_save_name = os.environ['HOME']+'/Position_Logs/'
if not os.path.exists(parent_save_name):
    os.makedirs(parent_save_name)
dat = datetime.datetime.now()
timestamp = str(dat.year).zfill(4)+'-'+str(dat.month).zfill(2)+'-'+str(dat.day).zfill(2)+'-'+str(dat.hour).zfill(2)+'-'+str(dat.minute).zfill(2)+'-'+str(dat.second).zfill(2)
outputdir = os.environ['HOME'] + '/Position_Logs/_' + timestamp
os.makedirs(outputdir)

#for debug
def print_pose(data):
    pos = data.name.index('wheel_robot')
    print "position:" + '\n' + '\tx:' + str(data.pose[pos].position.x) + '\n' + '\ty:' + str(data.pose[pos].position.y) + '\n' + '\tz:' + str(data.pose[pos].position.z) + '\n' + " orientation:" + '\n' + '\tx:' + str(data.pose[pos].orientation.x) + '\n' + '\ty:' + str(data.pose[pos].orientation.y) + '\n' + '\tz:' + str(data.pose[pos].orientation.z) + '\n' + "\033[8A",

# update xy position data
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

# is it used?
# may be able to be deleted
def save_xy():
    global x
    global y
    global pos

    pos.append([x,y])

# detect machine start, and define end time
# for now end time is defined as 245 secs advanced from start time
def time_start(data):
    if data.linear.x > 0.1 :
        sub_once.unregister()
        global start_time
        start_time = rospy.Time.now()
        global end_time
        end_time = start_time + rospy.Duration.from_sec(245)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            save_xy()
            if rospy.Time.now() - end_time > rospy.Duration.from_sec(1):
                with open(outputdir + '/pos.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(pos)
                sys.exit()
            rate.sleep()

#initialize recorder
def position_recording():
    
    rospy.init_node('course_out_surveillance', anonymous=True)
    rospy.Subscriber("/gazebo/model_states", ModelStates, xy_update, queue_size = 10)
    global sub_once
    sub_once = rospy.Subscriber("/cmd_vel", Twist, time_start)
    global pos
    pos = []
    global start_time
    start_time = rospy.Time.now()
    global end_time
    end_time = rospy.Time.now()+rospy.Duration.from_sec(10000)

    rospy.spin()


"""
    # spin() simply keeps python from exiting until this node is stopped
      rospy.spin()
"""


if __name__ == '__main__':
    try:
        position_recording()
    except rospy.ROSInterruptException:
        pass

