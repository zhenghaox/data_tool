#coding=utf-8
import os
import cv2
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position
path='/data_1/weizhang/data/SZ/1119/16252select/'
with open('/data_1/weizhang/data/SZ/1119/170_16252_500') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:-4]
    #print name   
    img=cv2.imread(line[:-1])
    #print srcpath+name+'.jpg'
    #img=cv2.imread(line[:-1])
    cv2.imwrite(path+name+'.jpg',img)