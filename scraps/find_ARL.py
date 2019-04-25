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
#srcpath='/media/e/0531suzhou_data/16252闯红灯/passcroped/'
#path='/media/e/0531suzhou_data/16252闯红灯/0614/selectimg2/'
f=open('/media/e/weizhang/data/baoding/0615/run.sh','w')
with open('/media/e/weizhang/data/baoding/0615/list') as jslist:
    lines=jslist.readlines()
for line in lines:
    name1 = line[-10:-1]
    name = line[-2:-1]
    if name == '@' or name1=='闯红灯':
        f.write('cp -rf '+line[:-1]+' .'+'\n')   
    #img=cv2.imread(srcpath+line[:-1])
    #print srcpath+line[:-1]
    #img=cv2.imread(line[:-1])
    #cv2.imwrite(path+line[:-1],img)
f.close()