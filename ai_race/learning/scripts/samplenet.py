import torch
import torch.nn as nn
import torch.nn.functional as F

class SampleNet(nn.Module):
    def __init__(self):
        super(SampleNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, 1, padding=1)
        self.conv2 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.conv3 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.conv4 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.conv5 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.fc1 = nn.Linear(76800, 128)
        self.fc2 = nn.Linear(128, 3)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = nn.MaxPool2d(kernel_size=2)(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = nn.MaxPool2d(kernel_size=2)(x)
        x = self.conv5(x)
        x = F.relu(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x

class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, 1, padding=1)
        self.conv2 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.conv3 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.conv4 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.conv5 = nn.Conv2d(16, 16, 3, 1, padding=1)
        self.fc1 = nn.Linear(int(76800/16), 128)
        self.fc2 = nn.Linear(128, 3)
        nn.init.kaiming_normal_(self.conv1.weight)
        nn.init.kaiming_normal_(self.conv2.weight)
        nn.init.kaiming_normal_(self.conv3.weight)
        nn.init.kaiming_normal_(self.conv4.weight)
        nn.init.kaiming_normal_(self.conv5.weight)
        nn.init.kaiming_normal_(self.fc1.weight)
        nn.init.kaiming_normal_(self.fc2.weight)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = nn.MaxPool2d(kernel_size=2)(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = nn.MaxPool2d(kernel_size=2)(x)
        x = self.conv3(x)
        x = F.relu(x)
        x = nn.MaxPool2d(kernel_size=2)(x)
        x = self.conv4(x)
        x = F.relu(x)
        x = nn.MaxPool2d(kernel_size=2)(x)
        x = self.conv5(x)
        x = F.relu(x)
        x = torch.flatten(x, 1)
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        return x
