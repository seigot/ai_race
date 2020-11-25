#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
import rosservice
from gazebo_msgs.srv import SetModelState, SetModelStateRequest, SetModelStateResponse
from std_srvs.srv import Empty, EmptyRequest
import dynamic_reconfigure.client

class jugemu:

    def __init__(self):
        rospy.wait_for_service('/gazebo/set_model_state')
        self.gazebo_teleport = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.gazebo_stop = rospy.ServiceProxy('/gazebo/pause_physics', Empty)
        rospy.Service('/jugemu/teleport', SetModelState, self.teleport)
        self.param_client = dynamic_reconfigure.client.Client("/gazebo", timeout=5, config_callback=self.param_callback)


    def param_callback(self, config):
        # print config
        pass


    def teleport(self, req):
        # まず重力を変更
        self.param_client.update_configuration({"gravity_z": -1.0})
        # 任意の位置にteleport
        req.model_state.model_name = 'wheel_robot'
        res = self.gazebo_teleport.call(req)
        if res.success == True:
            rospy.sleep(1)
            self.param_client.update_configuration({"gravity_z": -9.8})
            return
        else:
            self.gazebo_stop(EmptyRequest())
            rospy.logerr('can not teleport !!! stop sim !!')
        

def main():
    rospy.init_node('jugemu')
    jugemu()
    rospy.spin()

if __name__ == "__main__":
    main()
