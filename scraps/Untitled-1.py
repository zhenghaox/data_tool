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
f0=open('/media/e/weizhang/data/baoding/0809/0725/pingjie/0.list','w')
f1=open('/media/e/weizhang/data/baoding/0809/0725/pingjie/1.list','w')
f2=open('/media/e/weizhang/data/baoding/0809/0725/pingjie/2.list','w')
with open('/media/e/weizhang/data/baoding/0809/0725/pingjie/1625.txt') as jslist:
    lines=jslist.readlines()
for line in lines:
    id = line[-6:-5]
    print id
    if id == '0':
        f0.write(line)
    if id == '1':
        f1.write(line)
    if id == '2':
        f2.write(line)
