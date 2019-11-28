#coding=utf-8
import os
import cv2
import json
import random

def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

saveimgpath='/data_1/weizhang/data/all/ori/neg/img/'
savelabelpath='/data_1/weizhang/data/all/ori/neg/label/'
srcimgpath='/data_1/weizhang/data/all/ori/rmtra/'
with open('/data_1/weizhang/data/all/ori/rmtra.list') as jslist:
    lines=jslist.readlines()
for line in lines:
    name_1 = line[:-1][find_last(line[:-1], '/') + 1:]
    name=name_1[:find_last(name_1,'.')]
    img=cv2.imread(srcimgpath+name+'.jpg')
    if img is None:
        print srcimgpath+name+'.jpg'
        continue
    imgsz=[img.shape[1],img.shape[0]]
    Size=[1280,1280]
    MaxlightSize=150
    num_row=(imgsz[0]-MaxlightSize)/(Size[0]-MaxlightSize)+1
    num_col=(imgsz[1]-MaxlightSize)/(Size[1]-MaxlightSize)+1
    for i in range(0,num_row):
        for j in range(0,num_col/2):
            #j=0
            if random.random() > 0.1:
                continue
            imgrect=[max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])),max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])),min(Size[0],imgsz[0]),min(imgsz[1],Size[1])]
            imgcroped=img[max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])):max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1]))+min(imgsz[1],Size[1]),max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])):max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0]))+min(Size[0],imgsz[0]),:]
            if imgcroped.shape[1]!= Size[0] or imgcroped.shape[0]!= Size[1]:  
               print imgcroped.shape[1],imgcroped.shape[0]          
            savetxt=open(savelabelpath+name+'_1280_'+str(i)+'_'+str(j)+'.txt','w') 
            savetxt.write(str(imgcroped.shape[1])+' '+str(imgcroped.shape[0])+'\n')
            savetxt.write('0'+'\n')
            cv2.imwrite(saveimgpath+name+'_1280_'+str(i)+'_'+str(j)+'.jpg',imgcroped)