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
path='/data_1/weizhang/train/XC+BD/classify/classify/trainimg/'
with open('/data_1/weizhang/train/XC+BD/classify/classify/train.txt') as jslist:
    lines=jslist.readlines()
for line in lines:
    word1=line.strip()
    words=word1.split(' ')[0]
    niebie=word1.split(' ')[1]
    #print niebie
    name = words[:-1][find_last(line[:-1], '/') + 1:-3]
    print words
    #print name   
    img=cv2.imread('/'+words)
    #print srcpath+name+'.jpg'
    #img=cv2.imread(line[:-1])
    #print path+niebie+'/'+name+'.jpg'
    cv2.imwrite(path+niebie+'/'+name+'.jpg',img)