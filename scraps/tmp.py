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

#path='/media/d/work/weizhang/data/share/croped/'
f=open('/media/d/work/weizhang/oridata/0521/needcrop.txt','w')
f2=open('/media/d/work/weizhang/oridata/0521/noneedcrop.txt','w')
with open('/media/d/work/weizhang/oridata/0521/list.txt') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:-4]
    if name[-1:]!='3' and name[-1:]!='4' and name[-1:]!='5':
        f.write(line)
    else:
        f2.write(line)