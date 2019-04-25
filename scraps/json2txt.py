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
    #img=cv2.imread('/media/e/weizhang/data/BDdone/20180817/result/0816up1/mark/'+name+'.jpg')
    #print '/media/d/work/weizhang/trafficlight/JPEGImages/'+name+'.jpg'
    #imgsz=[img.shape[1],img.shape[0]]#w,h
    #imgcroped=img[:imgsz[1]/2,imgsz[0]/7:,:]
    #cv2.imwrite('/media/d/work/weizhang/trafficlight/cropeded/'+name+'.jpg',imgcroped)
    f=open('/media/e/weizhang/data/BDdone/20180817/result/0816up1/txt/'+name+'.txt','w')
    #f.write(str(len(obj))+'\n')
    for x1 in obj:
        #img=cv2.imread('/media/d/work/SSD/caffe/data/dataset_train_rgb/'+x1['path'][2:])
        #   name = line[:-1][find_last(line[:-1], '/') + 1:-8]
        #cv2.imwrite('/media/d/work/SSD/caffe/data/dataset_train_rgb/JPEGImages/'+name+'.jpg',img)
           #f=open('/media/d/work/weizhang/trafficlight/label/'+name+'.txt','w')
           #x2=x1['boxes']
           #f.write(str(len(obj))+'\n')
           #for num in range(0,len(obj)):
           #print x2[num]
               rect=x1['rect']
               ff.write(str(rect[0])+' '+str(rect[1])+' '+str(rect[2])+' '+str(rect[3])+'\n')
               xmin=rect[0]
               ymin=rect[1]
               xmax=rect[0]+rect[2]
               ymax=rect[1]+rect[3]               
               f.write(x1['label']+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
ff.close()
           