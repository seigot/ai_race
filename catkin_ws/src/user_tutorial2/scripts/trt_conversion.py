#!/usr/bin/env python
import time

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

import os
import argparse
import numpy as np
import time
from PIL import Image as IMG
from torch2trt import TRTModule
import cv2
from cv_bridge import CvBridge

model = models.resnet18()

device = 'cuda' if torch.cuda.is_available() else 'cpu'
def init_inference():

    flag_move = 0

    twist_pub = None

    global model
    global device
    model.fc = torch.nn.Linear(512, 3)
    model.eval()
    
    #model.load_state_dict(torch.load('/home/shiozaki/work/experiments/models/checkpoints/sim_race_joycon_ResNet18_6_epoch=20.pth'))
    model.load_state_dict(torch.load(args.pretrained_model))
    model = model.cuda()
    x = torch.ones((1, 3, 240, 320)).cuda()
    from torch2trt import torch2trt
    #model_trt = torch2trt(model, [x], max_batch_size=100, fp16_mode=True)
    model_trt = torch2trt(model, [x], max_batch_size=100)
    torch.save(model_trt.state_dict(), args.trt_model)
    #torch.save(model_trt.state_dict(), 'road_following_model_trt_half.pth')


def parse_args():
	# Set arguments.
	arg_parser = argparse.ArgumentParser(description="Autonomous with inference")
	
	arg_parser.add_argument("--pretrained_model", type=str)
	arg_parser.add_argument("--trt_model", type=str, default='road_following_model_trt.pth' )

	args = arg_parser.parse_args()

	return args

if __name__ == '__main__':
    args = parse_args()
    init_inference()
    try:
        inference_from_image()
    except rospy.ROSInterruptException:
        pass
