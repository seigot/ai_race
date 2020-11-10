from torch.utils.data import Dataset
import os
import io
import sys
import pandas as pd
import cv2

LABEL_IDX = 2
IMG_IDX = 1

class MyDataset(Dataset):
   def __init__(self, csv_file_path, root_dir, transform=None):
      self.image_dataframe = pd.read_csv(csv_file_path,engine='python')
      self.root_dir = root_dir
      self.transform = transform
      
   def __len__(self):
      return len(self.image_dataframe)
   
   def __getitem__(self, idx):
      label =[0]*3
      #for n in range(len(label)):
      #   label[n] = 0
      #print(label)
      label=self.image_dataframe.iat[idx, LABEL_IDX]
      img_name = self.image_dataframe.iat[idx, IMG_IDX]
      
      image = cv2.imread(img_name)
      if self.transform:
          image = self.transform(image)
      
      return image, label