#By Batu Kaan Ã–zen
from pathlib import Path
import argparse
import random
import numpy as np
import matplotlib.cm as cm
import torch
import cv2
import os
import matplotlib.pyplot as plt
import math
#Find Brightest Point
input_dir1 = "/home/imero/Desktop/ImeroBatuResearch/Images"
A = 0

for filename in os.listdir(input_dir1):
    A=A+1
    img = cv2.imread(os.path.join(input_dir1,filename))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    (   minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    #Removal noises
    equalizedGray = cv2.equalizeHist(gray)
    kernel = np.ones((3, 3),np.uint8)
    opening = cv2.morphologyEx(equalizedGray, cv2.MORPH_OPEN,kernel)
    ret, threshold = cv2.threshold(opening,120,255, cv2.THRESH_BINARY)
    
    #Find Rightest Leftes point on the top, point on the bottom
    gray =  threshold>75
    array = np.array(gray)*1
    Xmatrix = (array.sum(axis=0)>1)*1
    Ymatrix = (array.sum(axis=1)>1)*1
    CornerPointx1 = 0
    CornerPointx2 = 0
    CornerPointy1 = 0
    CornerPointy2 = 0
    for i in range(0,len(Xmatrix)):
        if (Xmatrix[i] ==1):
            CornerPointx1=i
            break
    for i in range(0,len(Xmatrix)):
        if (Xmatrix[len(Xmatrix)-1-i] ==1):
            CornerPointx2=len(Xmatrix)-1-i
            break
    
    for j in range(0,len(Ymatrix)):
        if (Ymatrix[j] ==1):
            CornerPointy1=j
            break
    
    for j in range(0,len(Ymatrix)):
        if (Ymatrix[len(Ymatrix)-1-j] ==1):
            CornerPointy2=len(Ymatrix)-1-j
            break

# Cropping Limit detection and checking the border condition, it is possible that our cropping location might be outof picture and  It can cause problems

    RectangeLengthX = CornerPointx2-CornerPointx1
    RectangeLenghtY = CornerPointy2-CornerPointy1
    
    RectengaleLocationx = (CornerPointx2+CornerPointx1)/2
    RectengaleLocationy = (CornerPointy1+CornerPointy2)/2

    CenterofX = maxLoc[1]
    CenterofY = maxLoc[0]
    cropMostRight = 0
    cropMostLeft = 0
    cropMostTop = 0
    cropMostBottom = 0
    organizer = 4
# 
    balancer =4
    CenterofX = (CenterofX + RectengaleLocationx*balancer)/((balancer+1))
    CenterofY = (CenterofY + RectengaleLocationy*balancer)/((balancer+1))
    

    if ((CenterofX + (RectangeLengthX/organizer)) >= gray.shape[1]):
        cropMostRight = gray.shape[1]-1
    else:
        cropMostRight = CenterofX + (RectangeLengthX/organizer)
        
    if ((CenterofX - (RectangeLengthX/organizer)) <= 0):
        cropMostLeft = 0
    else:
        cropMostLeft = CenterofX - (RectangeLengthX/organizer)
        
    if ((CenterofY- (RectangeLenghtY/organizer)) <= 0):
        cropMostBottom = 0
    else :
        cropMostBottom = CenterofY- (RectangeLenghtY/organizer)

    if ((CenterofY + (RectangeLenghtY/organizer)) >= gray.shape[0]):
        cropMostTop = gray.shape[0]
    else :
        cropMostTop = CenterofY + (RectangeLenghtY/organizer)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)       
    img[math.floor(cropMostBottom):math.floor(cropMostTop), math.floor(cropMostLeft):math.floor(cropMostRight),1] = gray[math.floor(cropMostBottom):math.floor(cropMostTop), math.floor(cropMostLeft):math.floor(cropMostRight)]

    plt.imshow(img)
    
    cv2.imwrite(str(A) +".jpeg",img)