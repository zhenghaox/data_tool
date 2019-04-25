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
f0=open('/media/e/weizhang/data/baoding/0809/0725/pingjie/cp.list','w')
f1=open('/media/e/weizhang/data/baoding/0809/0725/pingjie/js.list','w')
with open('/media/e/weizhang/data/baoding/0809/0725/pingjie/img.list') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[find_last(line,'/')+1:]
    cp=name.split('@')[0]
    f0.write(cp+'\n')
    f1.write(cp+'\n')