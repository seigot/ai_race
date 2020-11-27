#!/usr/bin/env python
import rospy

from gazebo_msgs.msg import ModelStates


def print_pose(data):
    pos = data.name.index('wheel_robot')
    print "position:" + '\n' + '\tx:' + str(data.pose[pos].position.x) + '\n' + '\ty:' + str(data.pose[pos].position.y) + '\n' + '\tz:' + str(data.pose[pos].position.z) + '\n' + " orientation:" + '\n' + '\tx:' + str(data.pose[pos].orientation.x) + '\n' + '\ty:' + str(data.pose[pos].orientation.y) + '\n' + '\tz:' + str(data.pose[pos].orientation.z) + '\n' + "\033[8A",

def course_out_surveillance():

    rospy.init_node('course_out_surveillance', anonymous=True)
    rospy.Subscriber("/gazebo/model_states", ModelStates, print_pose)
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        course_out_surveillance()
    except rospy.ROSInterruptException:
        pass
