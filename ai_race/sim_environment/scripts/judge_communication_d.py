#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import requests
import json
from time import sleep

import rosservice
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState

JUDGESERVER_REQUEST_URL="http://127.0.0.1:5000/judgeserver/request"
JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"
JUDGESERVER_GETSTATE_URL="http://127.0.0.1:5000/judgeserver/getState"

class JudgeCommunicationd(object):
    #jsonの内容
        # judge_info

    def __init__(self, judge_url, GameStateCallback_timer_duration):
        self.judge_url = judge_url
        self.vel_pub = rospy.Publisher('gamestate', String, queue_size=1)
        #print(GameStateCallback_timer_duration)
        rospy.Timer(rospy.Duration(GameStateCallback_timer_duration),
                    self.publishGameStateCallback)
        rospy.Timer(rospy.Duration(GameStateCallback_timer_duration),
                    self.postRosTimerCallback)
        self.tryCourseRecoveryCallback = rospy.Subscriber('gamestate', String, self.tryCourseRecoveryCallback)

    # http request
    def httpPostReqToURL(self, url, data):
        res = requests.post(url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res

    def postRosTimerCallback(self, state):
        url = JUDGESERVER_UPDATEDATA_URL
        req_data = {
            "current_ros_time": 0
        }
        req_data["current_ros_time"] = rospy.Time.now().to_sec()
        res = self.httpPostReqToURL(url, req_data)
        return res

    def publishGameStateCallback(self, state):
        resp = requests.get(self.judge_url)
        msg = resp.text
        #print(msg)
        self.vel_pub.publish(msg)
        return msg

    def tryCourseRecoveryCallback(self, state):
        # get status
        dic = json.loads(state.data)
        is_courseout = int(dic["judge_info"]["is_courseout"])
        CourseOutRecoveryLocationList = dic["field_info"]["CourseOutRecoveryLocationList"]
        LocationIdx = CourseOutRecoveryLocationList["index"]

        if is_courseout != 0:

            ## it's better to use semaphore--->
            ## post to judge server
            url = JUDGESERVER_UPDATEDATA_URL
            req_data = {
                "is_courseout": 0
            }
            res = self.httpPostReqToURL(url, req_data)

            ## courseout recovery (jugemu)
            rospy.wait_for_service('/jugemu/teleport')
            state_msg = ModelState()
            state_msg.model_name = ''
            state_msg.pose.position.x = LocationIdx[0][0]
            state_msg.pose.position.y = LocationIdx[0][1]
            state_msg.pose.position.z = LocationIdx[0][2]
            state_msg.pose.orientation.x = LocationIdx[0][3]
            state_msg.pose.orientation.y = LocationIdx[0][4]
            state_msg.pose.orientation.z = LocationIdx[0][5]
            state_msg.pose.orientation.w = LocationIdx[0][6]
            try:
                JugeMu_Teleport = rospy.ServiceProxy('/jugemu/teleport', SetModelState)
                resp = JugeMu_Teleport(state_msg)
                print(resp)
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e

            return res
            ## it's better to use semaphore---<

if __name__ == "__main__":
    rospy.init_node("judge_communication_d")

    # set param from launch param
    JUDGE_URL = rospy.get_param('~judge_url', 'http://127.0.0.1:5000')
    JUDGESERVER_GETSTATE_URL = JUDGE_URL + "/judgeserver/getState"
    TIMER_DURATION = rospy.get_param('~GameStateCallback_timer_duration', 0.25)
    JUDGECOMMUNICATIOND = JudgeCommunicationd(JUDGESERVER_GETSTATE_URL, TIMER_DURATION)

    rospy.spin()


