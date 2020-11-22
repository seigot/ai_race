#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import requests
import json
from time import sleep

class GameStatePublisher(object):
    #jsonの内容
        # judge_info

    def __init__(self, judge_url, GameStateCallback_timer_duration):
        self.judge_url = judge_url
        self.vel_pub = rospy.Publisher('gamestate', String, queue_size=1)
        #print(GameStateCallback_timer_duration)
        rospy.Timer(rospy.Duration(GameStateCallback_timer_duration),
                    self.publishGameStateCallback)

    def publishGameStateCallback(self, state):
        resp = requests.get(self.judge_url)
        msg = resp.text
        #print(msg)
        self.vel_pub.publish(msg)
        return msg


if __name__ == "__main__":
    rospy.init_node("judge_communication_d")

    # set param from launch param
    JUDGE_URL = rospy.get_param('~judge_url', 'http://127.0.0.1:5000')
    JUDGESERVER_GETSTATE_URL = JUDGE_URL + "/judgeserver/getState"
    TIMER_DURATION = rospy.get_param('~GameStateCallback_timer_duration', 0.25)
    GAMESTATEPUBLISHER = GameStatePublisher(JUDGESERVER_GETSTATE_URL, TIMER_DURATION)

    rospy.spin()


