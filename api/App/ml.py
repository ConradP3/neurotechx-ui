# -*- coding: utf-8 -*-
"""codefrag.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iWcebaWKG4f3uq6Cm7D_LIVsFkYrbflb

# Loose EEGNet
This notebook is a neural network that is based as much off of the EEGNet paper as I could understand.

---

# Import/Install all necessary packages and libraries
"""

import numpy as np

# from sklearn.metrics import roc_auc_score, precision_score, recall_score, accuracy_score, classification_report
# from sklearn.model_selection import train_test_split, KFold, RepeatedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
# from sklearn.utils import shuffle

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable, gradcheck
from torch.utils.data import TensorDataset, DataLoader

# from matplotlib import pyplot

import math

"""# Check for GPU availability and set device"""

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

"""# Load and format the data"""

torch.manual_seed(3)
torch.cuda.manual_seed(3)

channels = 7
timepoints = 500

# hyperparameters
freq, avg1stride, avg2stride = 250, (1, 4), (1, 8)
convstride = 1 # stride for each conv2D
conv1_neurons = 4
conv2_neurons = 8
conv3_neurons = 16
conv4_neurons = 8
kern1size = freq // 2
kern3size = 32
no_splits = 4

padding_needed = (kern1size - 1) / 2
conv1outx, conv1outy = (channels, (timepoints + (2 * padding_needed) - kern1size)/convstride + 1)

conv2outx, conv2outy = ((conv1outx - channels)/convstride + 1, conv1outy)
conv2outx, conv2outy = conv2outx // avg1stride[0], conv2outy // avg1stride[1]

conv3outx, conv3outy = (conv2outx, (conv2outy - kern3size)/convstride + 1)

conv4outx, conv4outy = (conv3outx, conv3outy)
conv4outx, conv4outy = (conv4outx // avg2stride[0], conv4outy // avg2stride[1])

flat1_in = int(conv4outx * conv4outy * conv4_neurons)

class ConstrainedConv2d(nn.Conv2d):
    def forward(self, input):
        return F.conv2d(input, self.weight.clamp(min=-1.0, max=1.0), self.bias, self.stride,
                        self.padding, self.dilation, self.groups)

CNNPoor = nn.Sequential(
    nn.ZeroPad2d((math.floor(padding_needed), math.ceil(padding_needed), 0, 0)),
    nn.Conv2d(1, conv1_neurons, (1, kern1size), bias=False),
    nn.ELU(),
    nn.BatchNorm2d(conv1_neurons),
    
    ConstrainedConv2d(conv1_neurons, conv2_neurons, (channels, 1), bias=False, groups=conv1_neurons),
    nn.ELU(),
    nn.BatchNorm2d(conv2_neurons),
    nn.AvgPool2d(avg1stride),
    nn.Dropout(),
    
    nn.Conv2d(conv2_neurons, conv3_neurons, (1, kern3size), bias=False, groups=conv2_neurons),
    nn.Conv2d(conv3_neurons, conv4_neurons, kernel_size=1, bias=False),
    nn.ELU(),
    nn.BatchNorm2d(conv4_neurons),
    nn.AvgPool2d(avg2stride),
    nn.Dropout(),
    
    nn.Flatten(),

    nn.Linear(flat1_in, 1),
    nn.Sigmoid(),
)

CNNPoor = CNNPoor.to(device)

loss_function = nn.BCELoss()
optimizer = optim.Adam(CNNPoor.parameters(), lr = 0.001)

def predict(chunk, filepath, model=CNNPoor):
    scaler = StandardScaler()
    for i in range(len(chunk)):
        chunk[i] = scaler.fit_transform(chunk[i])
    prediction = torch.from_numpy(prediction)
    prediction = prediction.unsqueeze(1)

    model.load_state_dict(torch.load(filepath))
    model.eval()
    with torch.no_grad():
        label = CNNPoor(prediction.float())
    label = torch.round(label)
    label = label.numpy()

    return label[0][0]
