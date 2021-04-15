#!/usr/bin/env python
# -*- coding: utf-8 -*-#
import rospy
import sys
import os
import subprocess
import math
import random
from gazebo_msgs.msg import ModelStates

PI = math.pi
poss=[]


def pos1(dl, dw):
    theta =dl/(8*PI)*(2*PI)
    wdx = dw*math.cos(theta)
    wdy = dw*math.sin(theta)
    x, y = rotate(4, 0, theta)
    return 2 + x + wdx, 4 + y + wdy

def pos2(dl, dw):
    return 2-dl, 8+dw

def pos3(dl, dw):
    x, y = pos1(dl, dw)
    x, y = rotate90(x-2, y-4)
    return x-2, y+4

def pos4(dl, dw):
    return -6-dw, 4-dl

def pos5(dl, dw):
    x, y = pos1(dl, dw)
    x, y = rotate90(x-2, y-4)
    x, y = rotate90(x, y)
    return x-2, y-4

def pos6(dl, dw):
    return -2+dl, -8-dw

def pos7(dl, dw):
    x, y = pos1(dl, dw)
    x, y = rotate90(x-2, y-4)
    x, y = rotate90(x, y)
    x, y = rotate90(x, y)
    return x+2, y-4

def rotate90(x, y):
    x, y = rotate(x, y, math.pi/2)
    return x, y

def rotate(x, y, rad):
    _x = x*math.cos(rad)-y*math.sin(rad)
    _y = x*math.sin(rad)+y*math.cos(rad)
    return _x, _y

def rand_odd():
    dl = random.uniform(1.5, 2 * PI - 1.5)
    dw = random.uniform(-0.4, 0.4)
    return dl, dw

def rand_even():
    dl = random.uniform(0.5, 4 - 0.5)
    dw = random.uniform(-0.4, 0.4)
    return dl, dw


def callback(data):
    global poss
    alp=['A','B','C','D','E','F','G']
    SubOnce.unregister()
    for i in range(7):

        # get MODEL_PATH
        stream = os.popen('echo $GAZEBO_MODEL_PATH | tr \':\' \'\n\' | grep "sim_world/models"')
        model_path = stream.read()
        if model_path == '\n':
            # parse error
            print("invalid environment parameter, check GAZEBO_MODEL_PATH")
            exit

        try :
            pos = data.name.index('cone_with_coin_'+alp[i])
        except :
            subprocess.Popen(['rosrun', 'gazebo_ros', 'spawn_model', '-file', model_path[:len(model_path)-1] + '/sankaku_cone_'+alp[i]+'/model.sdf', '-sdf', '-model', 'cone_'+alp[i], '-y', str(poss[i][1]), '-x', str(poss[i][0])])
            continue
        
        subprocess.call(['rosservice', 'call', 'gazebo/delete_model', 'cone_with_coin_'+alp[i]])
        subprocess.Popen(['rosrun', 'gazebo_ros', 'spawn_model', '-file',model_path[:len(model_path)-1] + '/sankaku_cone_'+alp[i]+'/model.sdf', '-sdf', '-model', 'cone_'+alp[i], '-y', str(poss[i][1]), '-x', str(poss[i][0])])
    quit()

def main():
    vals=[]
    flag_rand = True
    if flag_rand == True:
        dl, dw = rand_odd()
        vals.append([dl, dw])
        dl, dw = rand_even()
        vals.append([dl, dw])
        dl, dw = rand_odd()
        vals.append([dl, dw])
        dl, dw = rand_even()
        vals.append([dl, dw])
        dl, dw = rand_odd()
        vals.append([dl, dw])
        dl, dw = rand_even()
        vals.append([dl, dw])
        dl, dw = rand_odd()
        vals.append([dl, dw])
    else:
        vals.append([3,0.4])
        vals.append([3,0.4])
        vals.append([3,0.4])
        vals.append([3,0.4])
        vals.append([3,0.4])
        vals.append([3,0.4])
        vals.append([3,0.4])
    global poss
    x, y = pos1(vals[0][0],vals[0][1])
    poss.append([x, y])
    x, y = pos2(vals[1][0],vals[1][1])
    poss.append([x, y])
    x, y = pos3(vals[2][0],vals[2][1])
    poss.append([x, y])
    x, y = pos4(vals[3][0],vals[3][1])
    poss.append([x, y])
    x, y = pos5(vals[4][0],vals[4][1])
    poss.append([x, y])
    x, y = pos6(vals[5][0],vals[5][1])
    poss.append([x, y])
    x, y = pos7(vals[6][0],vals[6][1])
    poss.append([x, y])

if __name__ == '__main__':
    main()
    rospy.init_node('spawn_cones', anonymous=True)
    SubOnce = rospy.Subscriber('/gazebo/model_states',ModelStates, callback, queue_size=1)

    rospy.spin()
