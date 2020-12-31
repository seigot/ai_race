#!/usr/bin/env python
import rospy
import rospkg
import time
import subprocess

# rosrun learning rosnode_inference_from_image.py _trt_model:="default_path"
# roslaunch learning inference_from_image.launch trt_model:=$HOME/ai_race_data_sample/model/plane/sample_plane_trt.pth

def main():
    # get path
    rospack = rospkg.RosPack()
    learning_pkg_path = rospack.get_path('learning')
    trt_model_path = rospy.get_param('~trt_model')
    image_topic_name = rospy.get_param('~image_topic_name')
    #image_topic_name = "/front_camera/image_exp"

    # call command
    inference_from_image_path = learning_pkg_path + '/scripts/inference_from_image.py'
    command = 'python' + ' ' + inference_from_image_path + ' ' + '--trt_module --trt_model' + ' ' + trt_model_path + ' ' + "--image_topic_name" +' ' + image_topic_name
    print(command)
    subprocess.call(command.split())

if __name__ == "__main__":
    rospy.init_node("rosnode_inference_from_image")
    main()
