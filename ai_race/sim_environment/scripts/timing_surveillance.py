#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Bool
from std_msgs.msg import Float32
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Range
import requests
import json

flag = False

JUDGESERVER_REQUEST_URL="http://127.0.0.1:5000/judgeserver/request"
JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"
JUDGESERVER_GETSTATE_URL="http://127.0.0.1:5000/judgeserver/getState"

def httpPostReqToURL(url, data):
    res = requests.post(url,
                        json.dumps(data),
                        headers={'Content-Type': 'application/json'}
                        )
    return res

def start_time(data):

    url = JUDGESERVER_REQUEST_URL
    if data.linear.x != 0 :
        req_data = {"change_state": "start"}
        res = httpPostReqToURL(url, req_data)
        print("start!!")
        sub_once.unregister()
        rospy.Subscriber("/ir_sensor", Range, lap_time)

def lap_time(data):
    global flag
    if data.range != 2.0 and flag == True :
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {"lap_count": 1}
        res = httpPostReqToURL(url, req_data)
        print("lap +1")
        flag = False
    elif data.range == 2.0 and flag == False :
        flag = True

def servo_commands():

    rospy.init_node('timing_surveillance', anonymous=True)

    global sub_once
    sub_once = rospy.Subscriber("/cmd_vel", Twist, start_time)
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        servo_commands()
    except rospy.ROSInterruptException:
        pass
