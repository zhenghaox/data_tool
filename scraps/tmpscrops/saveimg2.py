#coding=utf-8
import os
import cv2
import shutil
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


outpath='/data_1/weizhang/data/红绿灯分类测试/0711/data/train/'
with open('/data_1/weizhang/data/all/classify/train_new.txt') as jslist:
    lines=jslist.readlines()
for line in lines:
    words=line.split(' ')
    name = words[0][find_last(words[0][:-1], '/') + 1:-4]
    lb=words[1][:-1]
    if not os.path.exists(outpath+lb):
        os.mkdir(outpath+lb)    
    #print words[0]
    if os.path.exists('/'+words[0]):
        shutil.copy('/'+words[0],outpath+lb+'/'+name+'.jpg')