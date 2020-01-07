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

saveimgpath='/data_1/weizhang/data/all/ori/neg/cutall/'
savelabelpath='/data_1/weizhang/data/all/ori/neg/txtall/'
srcimgpath='/data_1/weizhang/data/all/ori/rmtra/'
#jspath='/data_1/weizhang/data/all/后加/lichao_xiaolan_0919/json'
if not os.path.exists(saveimgpath):
    os.mkdir(saveimgpath)
if not os.path.exists(savelabelpath):
    os.mkdir(savelabelpath)
sizeses={1,2,3,4,320,640,960,1280}
lines=os.listdir(srcimgpath)
for line1 in lines:
    # if random.random() > 0.4:
    #     continue
    line=os.path.join(srcimgpath,line1)
    name=line1[:find_last(line1,'.')]
    print name
    img=cv2.imread(line)
    imgsz=[img.shape[1],img.shape[0]]
    for sizes in sizeses:
        if sizes < 300:
            Size=[img.shape[1]/sizes,img.shape[0]/sizes]
        else:
            Size=[sizes,sizes]
        #print imgsz,Size
        MaxlightSize=150
        if Size[0] <=MaxlightSize or Size[1] <=MaxlightSize :
            continue
        num_row=(imgsz[0]-MaxlightSize)/(Size[0]-MaxlightSize)+1
        num_col=(imgsz[1]-MaxlightSize)/(Size[1]-MaxlightSize)+1
        for i in range(0,num_row):
            for j in range(0,max(num_col/2,1)):
                if random.random() > 0.1:
                    continue  
                imgrect=[max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])),max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])),min(Size[0],imgsz[0]),min(imgsz[1],Size[1])]
                imgcroped=img[max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])):max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1]))+min(imgsz[1],Size[1]),max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])):max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0]))+min(Size[0],imgsz[0]),:]
                if imgcroped.shape[1]!= Size[0] or imgcroped.shape[0]!= Size[1]:  
                    #print imgcroped.shape[1],imgcroped.shape[0]
                    pass            
                #print num
                savetxt=open(savelabelpath+name+'_'+str(sizes)+'_'+str(i)+'_'+str(j)+'.txt','w')
                cv2.imwrite(saveimgpath+name+'_'+str(sizes)+'_'+str(i)+'_'+str(j)+'.jpg',imgcroped)