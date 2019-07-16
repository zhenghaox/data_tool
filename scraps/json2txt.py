import yaml
import os
import cv2
import json
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

with open('/media/e/weizhang/data/BDdone/20180817/result/0816up1/jslist') as jslist:
    lines=jslist.readlines()
ff=open('/media/e/weizhang/data/BDdone/20180817/result/0816up1/txtlist.txt','w')
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:line.find('.')]
    f1=open(line[:-1])
    x=json.load(f1)
    obj=x['objects']
    f=open('/media/e/weizhang/data/BDdone/20180817/result/0816up1/txt/'+name+'.txt','w')
    for x1 in obj:
        rect=x1['rect']
        ff.write(str(rect[0])+' '+str(rect[1])+' '+str(rect[2])+' '+str(rect[3])+'\n')
        xmin=rect[0]
        ymin=rect[1]
        xmax=rect[0]+rect[2]
        ymax=rect[1]+rect[3]               
        f.write(x1['label']+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
ff.close()
           