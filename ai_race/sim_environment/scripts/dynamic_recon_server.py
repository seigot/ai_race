#!/usr/bin/env python

import rospy
import os
from dynamic_reconfigure.server import Server

try:
    from sim_environment.cfg import simEnvDynamicReconConfig
except ImportError:
    print("Warning: No module named sim_environment.cfg")
    print("dynamic_recon_server init process end...")
    os._exit(0)

def callback(config, level):
    rospy.loginfo("""Reconfigure Request: {max_speed_coeff}""".format(**config))
    return config

if __name__ == "__main__":
    rospy.init_node("dynamic_recon_server_node", anonymous = False)

    srv = Server(simEnvDynamicReconConfig, callback)
    rospy.spin()

