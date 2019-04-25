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

saveimgpath='/data_1/weizhang/data/红绿灯try/up/'
savelabelpath='/data_1/weizhang/data/红绿灯try/label/'
srcimgpath='/data_1/weizhang/data/红绿灯try/img/'

if not os.path.exists(saveimgpath):
    os.mkdir(saveimgpath)
if not os.path.exists(savelabelpath):
    os.mkdir(savelabelpath)
with open('/data_1/weizhang/data/红绿灯try/jsonlist') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:line.find('.jpg')]
    jsfile=open(line[:-1])
    jsf=json.load(jsfile)
    obj=jsf['objects']
    img=cv2.imread(srcimgpath+name+'.jpg')
    if img is None:
        print srcimgpath+name+'.jpg'
        continue
    imgsz=[img.shape[1],img.shape[0]]
    xmin=99999
    xmax=0
    ymin=99999
    ymax=0
    for x in obj:
        lbrect=x['rect']
        lb=x['label']
        if lb=='feijidongchedeng':
            continue
        # if lbrect[2]>lbrect[3]:
        #     lb=lb+'-heng'
        # else:
        #     lb=lb+'-shu'
        #print lbrect[0],lbrect[1],lbrect[2]
        x_new=int(lbrect[0])
        y_new=int(lbrect[1])
        w_new=int(lbrect[2])
        h_new=int(lbrect[3])
        if xmin>x_new:
            xmin=x_new
        if ymin>y_new:
            ymin=y_new
        if xmax<x_new+w_new:
            xmax=x_new+w_new
        if ymax<y_new+h_new:
            ymax=y_new+h_new
    if(ymax>imgsz[1]/2):
        continue
    xmin=max(xmin-50,0)
    ymin=max(ymin-25,0)
    xmax=min(xmax+50,imgsz[0])
    ymax=min(ymax+25,imgsz[1])
    img_up=img[:imgsz[1]/2,:,:]
    img_draw=img[:imgsz[1]/2,:,:]
    savetxt=open(savelabelpath+name+'_up_'+'.txt','w')
    savetxt.write('1\n')
    savetxt.write('trafficlight '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
    cv2.imwrite(saveimgpath+name+'_up_'+'.jpg',img_up)
    cv2.rectangle(img_draw,(xmin,ymin),(xmax,ymax),(0,0,255))
    cv2.imwrite('/data_1/weizhang/data/红绿灯try/mark1/'+name+'_up_'+'.jpg',img_draw)

