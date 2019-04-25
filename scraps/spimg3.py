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

def str2float(s):  
    def char2num(s):  
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]  
    n = s.index('.')  
    return reduce(lambda x,y:x*10+y,map(char2num,s[:n]+s[n+1:]))/(10**n)  

with open('/media/e/weizhang/data/BDdone/all/jsonlist') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:-5]
    jsfile=open(line[:-1])
    jsf=json.load(jsfile)
    obj=jsf['objects']
    img=cv2.imread('/media/e/weizhang/data/BDdone/all/img/'+name)#+'.jpg')
    imgsz=[img.shape[1],img.shape[0]]
    Size=[960,960]
    MaxlightSize=150
    num_row=(imgsz[0]-MaxlightSize)/(Size[0]-MaxlightSize)+1
    num_col=(imgsz[1]-MaxlightSize)/(Size[1]-MaxlightSize)+1
    for i in range(0,num_row):
        for j in range(0,num_col):
            imgrect=[max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])),max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])),min(Size[0],imgsz[0]),min(imgsz[1],Size[1])]
            imgcroped=img[max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])):max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1]))+min(imgsz[1],Size[1]),max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])):max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0]))+min(Size[0],imgsz[0]),:]
            if imgcroped.shape[1]!= Size[0] or imgcroped.shape[0]!= Size[1]:  
               print imgcroped.shape[1],imgcroped.shape[0]  
            num=0           
            datalist=[]
            for x in obj:
                lbrect=x['rect']
                lb=x['label']    
                x_new=float(lbrect[0])-imgrect[0]
                y_new=float(lbrect[1])-imgrect[1]
                w_new=float(lbrect[2])
                h_new=float(lbrect[3])
                if x_new>=-5 and y_new>=-5 and x_new+w_new<=Size[0]+5 and y_new+h_new<=Size[1]+5:                    
                    num=num+1
                    newlist=[lb,str(int(x_new)),str(int(y_new)),str(int(x_new+w_new)),str(int(y_new+h_new))]
                    datalist.append(newlist)
            if len(datalist)>0:
                savetxt=open('/media/e/weizhang/data/BDdone/all/0816label/'+name+'_960_'+str(i)+'_'+str(j)+'.txt','w')
                savetxt.write(str(num)+'\n')
                for t in range(0,len(datalist)):
                    savetxt.write(datalist[t-1][0]+' '+datalist[t-1][1]+' '+datalist[t-1][2]+' '+datalist[t-1][3]+' '+datalist[t-1][4]+'\n')
                cv2.imwrite('/media/e/weizhang/data/BDdone/all/0816img/'+name+'_960_'+str(i)+'_'+str(j)+'.jpg',imgcroped)