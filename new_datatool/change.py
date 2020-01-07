#!/usr/bin/python
# -*- coding=utf-8 -*-
import os
import os.path
from math import *
import math
import random
import cv2
import re
import shutil
import json
import numpy as np
from PIL import Image, ImageEnhance
import imutils

#输出不违法图片
def transLegalImg():
    txt1 = "/data_1/weizhang/data/错图积累/res_1625.txt"
    filesSrc = "/data_1/weizhang/data/错图积累/无锡所/1625/"
    files = "/data_1/weizhang/data/错图积累/无锡所/2/"
    s1 = []
    s1_ = []
    f1 = open(txt1,'r')
    for lines in f1:
        ls = lines.strip('\n').split('#')
        s1.append(ls[0])
        s1_.append(ls[1])

        if ls[1] == "1":
            shutil.copy2(filesSrc + ls[0] + ".jpg", files)


#不违法改成违法
def transLegal2Illegal():
    txt1 = "/data_2/data/1204/wuxi/res/res_1625.txt"
    txt2 = "/data_2/data/1204/wuxi/res/红绿灯_违法.list"
    txtSave = "/data_2/data/1204/wuxi/res/res_1625_.txt"
    f1 = open(txt1,'r')
    fw = open(txtSave,'w')
    for lines in f1:
        ls = lines.strip('\n').split('#')
        f2 = open(txt2,'r')
        flag = True
        for lines2 in f2:
            ls2 = lines2.strip('\n').split('.')
            if ls[0] == ls2[0] and ls[1] == '1':
                str1 =  lines[0] + "#" + "0\n"
                flag = False
                break
        if flag:
            str1 = lines
        #print(str1)
        fw.write(str1)

if __name__ == '__main__':
    #transLegal2Illegal()
    transLegalImg()
    