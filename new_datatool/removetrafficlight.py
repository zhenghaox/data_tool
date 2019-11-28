#coding=utf-8
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
srcimgpath='/data_1/weizhang/data/all/后加/lichao_xiaolan_0919/mark/'
jspath='/data_1/weizhang/data/all/后加/lichao_xiaolan_0919/json'
path='/data_1/weizhang/data/all/ori/rmtra/'
lines=os.listdir(jspath)
#with open('/data_1/weizhang/data/all/ori/jslist') as jslist:
#    lines=jslist.readlines()
for line1 in lines:
    line=os.path.join(jspath,line1)
    name=''
    name = line[find_last(line, '/') + 1:-9]
    jsfile=open(line)
    jsf=json.load(jsfile)
    obj=jsf['objects']
    img=None
    img=cv2.imread(srcimgpath+name+'.jpg')
    if img is None:
        print srcimgpath+name+'.jpg'
        name = line[find_last(line, '/') + 1:-5]
        img=cv2.imread(srcimgpath+name+'.jpg')
        if img is None:
            print srcimgpath+name+'.jpg'
            continue
    name=name.strip()
    imgsz=[img.shape[1],img.shape[0]]
    num=0
    for x in obj:
        num=num+1
        lbrect=x['rect']
        lb=x['label']
        cv2.rectangle(img,(int(lbrect[0]),int(lbrect[1])),(int(lbrect[0])+int(lbrect[2]),int(lbrect[1])+int(lbrect[3])),(0,0,0),-1)
    cv2.imwrite(path+name+'.jpg',img)

    