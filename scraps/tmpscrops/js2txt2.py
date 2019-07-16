#coding=utf-8
import os
#import cv2
import json
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

if __name__ == "__main__":

    jspath='/data_1/weizhang/data/铭牌文件检测/json'
    txtpath='/data_1/weizhang/data/铭牌文件检测/text'
    lists=os.listdir(jspath)
    for line in lists:
        name = line[:line.find('.jpg')]
        jsfilepath=os.path.join(jspath,line)
        f1=open(jsfilepath)
        x=json.load(f1)
        obj=x['objects']
        f=open(txtpath+'/'+name+'.txt','w')
        for xx in obj:
            pts=xx['polygon']
            p1=pts[0]
            p2=pts[1]
            p3=pts[2]
            p4=pts[3]
            #print p1,p2,p3,p4  
            x1=int(p1[0])
            y1=int(p1[1])  
            x2=int(p2[0])
            y2=int(p2[1])
            x3=int(p3[0])
            y3=int(p3[1])
            x4=int(p4[0])
            y4=int(p4[1])
            xmin=min(x1,x2,x3,x4)
            ymin=min(y1,y2,y3,y4)
            xmax=max(x1,x2,x3,x4)
            ymax=max(y1,y2,y3,y4)
            #print xmin,ymin,xmax,ymax                      
            f.write(xx['label']+' '+str(x1)+' '+str(y1)+' '+str(x2)+' '+str(y2)+' '+str(x3)+' '+str(y3)+' '+str(x4)+' '+str(y4)+' '+str(xmin)+' '+str(ymin)+' '+str(xmax)+' '+str(ymax)+'\n')
       # f.close