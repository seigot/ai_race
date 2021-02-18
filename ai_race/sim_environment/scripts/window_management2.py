#!/usr/bin/env python
import rospy
import time
import subprocess
import sys


from sensor_msgs.msg import Image

args = sys.argv
args_parsed = {}
cnt = 0

def start_trigger(data):
    global cnt
    print((subprocess.check_output(['echo "count"'], shell=True))[0:5])

    # recieve error until all windows are launched
    try :
        if args_parsed["arrow"] :
            front_id = subprocess.check_output(['xdotool search --onlyvisible --name "/front_camera_w_arrow/image_raw"'], shell=True)
        else :
            front_id = subprocess.check_output(['xdotool search --onlyvisible --name "/front_camera/image_raw"'], shell=True)
        
        if args_parsed["play"]:
            godeye_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera_w_champ/image_raw"'], shell=True)
        else :
            godeye_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera/image_raw"'], shell=True)
        stopwatch_id = subprocess.check_output(['xdotool search --onlyvisible --name "Python Stop watch"'], shell=True)
        godeye_perspective_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera_perspective/image_raw"'], shell=True)
    finally :
        pass
    try :
        front_id
        godeye_id
        stopwatch_id
        if cnt > 1:
            sub_once.unregister()
            if args_parsed["play"]:
                godeye_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera_w_champ/image_raw"'], shell=True)
            else :
                godeye_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera/image_raw"'], shell=True)
                
            if args_parsed["arrow"] :
                front_id = subprocess.check_output(['xdotool search --onlyvisible --name "/front_camera_w_arrow/image_raw"'], shell=True)
            else :
                front_id = subprocess.check_output(['xdotool search --onlyvisible --name "/front_camera/image_raw"'], shell=True)
            godeye_perspective_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera_perspective/image_raw"'], shell=True)
            #surveillance_id = subprocess.check_output(['xdotool search --onlyvisible --name "/surveillance_camera/image_raw"'], shell=True)
            stopwatch_id = subprocess.check_output(['xdotool search --onlyvisible --name "Python Stop watch"'], shell=True)
            
            subprocess.call(['xdotool windowmove ' + str(front_id[0:8]) + ' 670 67'], shell=True)
            subprocess.call(['xdotool windowmove ' + str(stopwatch_id[0:8]) + ' 0 0'], shell=True)
            #subprocess.call(['xdotool windowmove ' + str(surveillance_id[0:8]) + ' 0 300'], shell=True)
            subprocess.call(['xdotool windowmove ' + str(godeye_id[0:8]) + ' 0 340'], shell=True)
            subprocess.call(['xdotool windowmove ' + str(godeye_perspective_id[0:8]) + ' 710 340'], shell=True)
            #subprocess.call(['xdotool windowmove ' + str(keyboard_id[0:8]) + ' 0 600'], shell=True)
            #subprocess.call(['xdotool windowactivate ' + str(keyboardcon_id[0:8])], shell=True)
            subprocess.call(['xdotool windowsize ' + str(godeye_id[0:8]) + ' 640 480'], shell=True)
            subprocess.call(['xdotool windowsize ' + str(godeye_perspective_id[0:8]) + ' 720 480'], shell=True)

            sys.exit()
        else :
            cnt +=1
    finally :
        pass

def window_management():
    rospy.init_node('window_management', anonymous=True)

    global sub_once
    sub_once = rospy.Subscriber("/godeye_camera/image_raw", Image, start_trigger)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

# roslaunch doesn't match arg_parser module, because of some extra arguments added by roslaunch
def parse_args():
    # Set arguments.
    global args_parsed
    if "-play" in args:
        args_parsed["play"] = True
    else:
        args_parsed["play"] = False
    if "-arrow" in args:
        args_parsed["arrow"] = True
    else:
        args_parsed["arrow"] = False

    return args
if __name__ == '__main__':
    parse_args()
    try:
        window_management()
    except rospy.ROSInterruptException:
        pass
