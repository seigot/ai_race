# -*- coding: utf-8 -*-

import sys
import os

import rosbag
import cv2
import csv
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


def output_files(bagFilename):

    inputfile = os.path.basename(bagFilename)
    inputdir = os.path.dirname(bagFilename)
    outputdir = inputdir + '/Images_from_rosbag/' + inputfile[0:len(inputfile)-4]
    cnt = 2
    if os.path.exists(outputdir) == True :
        outputdir = outputdir + '_' + str(cnt)
        while (os.path.exists(outputdir)):
            cnt += 1
            outputdir = outputdir[0:len(outputdir)-2] + '_' + str(cnt)
    outputimagedir = outputdir + '/images'
    os.makedirs(outputdir)
    #os.makedirs(outputimagedir)
    outputcsv = outputdir + '/' + inputfile[0:len(inputfile)-4] + '.csv'
    
    timestamps = [];
    images = [];
    csv_out = [];

    num = 0
    for topic, msg, t in  rosbag.Bag(bagFilename).read_messages():
        if topic == '/front_camera/image_raw':
            #timestamps.append(t.to_sec())
            #images.append( CvBridge().imgmsg_to_cv2(msg, "bgr8") )
            #image_path = outputimagedir + '/image_no.{:0>5}.jpg'.format(str(num))
            #cv2.imwrite(image_path, images[num])
            #prev = "image"
            csv_out.append([t.to_sec(), "image" ])
        elif topic == '/cmd_vel':
            if True :
                #cmd = str(int(msg.angular.z*100+256))
                cmd = str(int(msg.angular.z+1))
                #print(str(num-1))
                #print(image_path)
                #print(cmd)
                csv_out.append([t.to_sec(),cmd])
                num = num +1
            prev = "cmd"
    with open(outputcsv, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(csv_out)


if __name__ == '__main__':
    if len(sys.argv) < 2 :
        print "rosbagファイルを入力してください"
        exit()
    else :
        output_files(sys.argv[1])
