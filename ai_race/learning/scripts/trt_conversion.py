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

from samplenet import SampleNet, SimpleNet

import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../config")
import learning_config

DISCRETIZATION = learning_config.Discretization_number

device = 'cuda' if torch.cuda.is_available() else 'cpu'

def init_inference():
    global device
    if args.model == 'resnet18':
        model = models.resnet18()
        model.fc = torch.nn.Linear(512, DISCRETIZATION)
    elif args.model == 'samplenet':
        model = SampleNet(DISCRETIZATION)
    elif args.model == 'simplenet':
        model = SimpleNet(DISCRETIZATION)
    else:
        raise NotImplementedError()
    model.eval()
    
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
	
    arg_parser.add_argument("--model", type=str, default='resnet18')
    arg_parser.add_argument("--pretrained_model", type=str)
    arg_parser.add_argument("--trt_model", type=str, default='road_following_model_trt.pth' )

    args = arg_parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    print("process start...")

    init_inference()

    print("finished successfully.")
    print("model_path: " + args.trt_model)
    os._exit(0)
