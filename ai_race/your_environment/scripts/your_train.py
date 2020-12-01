'''Train CIFAR10 with PyTorch.'''
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

import os
import io
import argparse
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split

def main():
        print("This is your train script.")
        print("As first step, recommend to copy and use sample train.py. (ai_race/ai_race/learning/scripts/train.py)")

if __name__ == "__main__":
	main()
