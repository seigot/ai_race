#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
import json
import sys

class Sample():

    def __init__(self):
        # war state
        topicname_war_state = "gamestate"
        self.gamestate = rospy.Subscriber(topicname_war_state, String, self.stateCallback)
        self.FLAG = 0
        self.COUNT = 0

    def stateCallback(self, state):

        dic = json.loads(state.data)
        self.time = int(dic["judge_info"]["time"])
        self.lap_count = int(dic["judge_info"]["lap_count"])
        self.courseout_count = int(dic["judge_info"]["courseout_count"])

        print('time=%d' % self.time)
        print('lap_count=%d' % self.lap_count)
        print('courseout_count=%d' % self.courseout_count)

        self.FLAG = 1
        
    def strategy(self):
        # Main Loop --->
        r = rospy.Rate(100)
        while not rospy.is_shutdown():
            r.sleep()
            if self.FLAG > 0:
                sys.exit(0)

            # error exit
            # the case of "no state callback is published".
            # basically state callback come in 1s,
            # but sometimes no state callback. when it occurs, go exit..
            self.COUNT += 1
            if self.COUNT > 3000:
                sys.exit(0)

if __name__ == '__main__':
    rospy.init_node('sample')
    bot = Sample()
    bot.strategy()

