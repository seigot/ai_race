#!/usr/bin/env python
import rospy
import time
import subprocess
import sys

from sensor_msgs.msg import Image


cnt = 0

def start_trigger(data):
    global cnt
    print((subprocess.check_output(['echo "count"'], shell=True))[0:5])
    if cnt > 3:
        sub_once.unregister()
        godeye_id = subprocess.check_output(['xdotool search --onlyvisible --name "/godeye_camera/image_raw"'], shell=True)
        front_id = subprocess.check_output(['xdotool search --onlyvisible --name "/front_camera/image_raw"'], shell=True)
        surveillance_id = subprocess.check_output(['xdotool search --onlyvisible --name "/surveillance_camera/image_raw"'], shell=True)
        stopwatch_id = subprocess.check_output(['xdotool search --onlyvisible --name "Python Stop watch"'], shell=True)
        #keyboard_id = subprocess.check_output(['xdotool search --onlyvisible --name "keyboard"'], shell=True)
        #keyboardcon_id = subprocess.check_output(['xdotool search --onlyvisible --name "keyboardcon"'], shell=True)
        #print("get id:" + godeye_id)
        #print("get id:" + front_id)
        #print("get id:" + surveillance_id)
        #print("get id:" + stopwatch_id)
        #print('xdotool windowmove ' + str(front_id[0:8]) + ' 0 0')
        subprocess.call(['xdotool windowmove ' + str(front_id[0:8]) + ' 0 0'], shell=True)
        subprocess.call(['xdotool windowmove ' + str(stopwatch_id[0:8]) + ' 400 0'], shell=True)
        subprocess.call(['xdotool windowmove ' + str(surveillance_id[0:8]) + ' 0 300'], shell=True)
        subprocess.call(['xdotool windowmove ' + str(godeye_id[0:8]) + ' 400 300'], shell=True)
#        subprocess.call(['xdotool windowmove ' + str(keyboard_id[0:8]) + ' 0 600'], shell=True)
#        subprocess.call(['xdotool windowactivate ' + str(keyboardcon_id[0:8])], shell=True)
        subprocess.call(['xdotool windowsize ' + str(godeye_id[0:8]) + ' 640 480'], shell=True)
        sys.exit()
    else :
        cnt +=1

def window_management():
    rospy.init_node('window_management', anonymous=True)

    global sub_once
    sub_once = rospy.Subscriber("/godeye_camera/image_raw", Image, start_trigger)
    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        window_management()
    except rospy.ROSInterruptException:
        pass
