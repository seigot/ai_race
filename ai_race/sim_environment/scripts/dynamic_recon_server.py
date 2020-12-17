#!/usr/bin/env python

import rospy

from dynamic_reconfigure.server import Server
from sim_environment.cfg import simEnvDynamicReconConfig

def callback(config, level):
    rospy.loginfo("""Reconfigure Request: {max_speed_coeff}""".format(**config))
    return config

if __name__ == "__main__":
    rospy.init_node("dynamic_recon_server_node", anonymous = False)

    srv = Server(simEnvDynamicReconConfig, callback)
    rospy.spin()

