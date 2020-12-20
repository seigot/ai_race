#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
rosservice call /jugemu/teleport "model_state:
  model_name: ''
  pose:
    position:
      x: 0.0
      y: 0.0
      z: 0.3
    orientation:
      x: 0.0
      y: 0.0
      z: 0.0
      w: 0.0
  twist:
    linear:
      x: 0.0
      y: 0.0
      z: 0.0
    angular:
      x: 0.0
      y: 0.0
      z: 0.0
  reference_frame: ''"
'''
# このsrvを呼ぶことで
# 任意の位置に移動
import rospy
import rosservice
from gazebo_msgs.srv import SetModelState, SetModelStateRequest, SetModelStateResponse
from std_srvs.srv import Empty, EmptyRequest
import dynamic_reconfigure.client

import json
import requests

JUDGESERVER_UPDATEDATA_URL="http://127.0.0.1:5000/judgeserver/updateData"

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

    # http request
    def httpPostReqToURL(self, url, data):
        res = requests.post(url,
                            json.dumps(data),
                            headers={'Content-Type': 'application/json'}
                            )
        return res


    def teleport(self, req):
        # まず重力を変更
        # self.param_client.update_configuration({"gravity_z": -1.0})
        # 任意の位置にteleport
        req.model_state.model_name = 'wheel_robot'
        res = self.gazebo_teleport.call(req)
        
        if res.success == False:
            self.gazebo_stop(EmptyRequest())
            rospy.logerr('can not teleport !!! stop sim !!')
            srv_res = SetModelStateResponse()
            srv_res.status_message = 'can not teleport !!! stop sim !!'
            return srv_res
        else:
            url = JUDGESERVER_UPDATEDATA_URL
            req_data = {
                "recovery_count": 1
            }
            res = self.httpPostReqToURL(url, req_data)
            # rospy.sleep(1)
            # self.param_client.update_configuration({"gravity_z": -9.8})
            srv_res = SetModelStateResponse()
            srv_res.status_message = 'success'
            srv_res.success = True
            return srv_res
        

def main():
    rospy.init_node('jugemu')
    jugemu()
    rospy.spin()

if __name__ == "__main__":
    main()
