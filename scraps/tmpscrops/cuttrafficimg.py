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

saveimgpath='/data_1/weizhang/data/all/cut/img_all/'
savelabelpath='/data_1/weizhang/data/all/cut/label_all/'
srcimgpath='/data_1/weizhang/data/all/ori/mark/'
sizes='whole'
if not os.path.exists(saveimgpath):
    os.mkdir(saveimgpath)
if not os.path.exists(savelabelpath):
    os.mkdir(savelabelpath)
with open('/data_1/weizhang/data/all/ori/jslist') as jslist:
    lines=jslist.readlines()
for line in lines:
    if(line.find('.jpg')==-1):
        name = line[:-1][find_last(line[:-1], '/') + 1:line.find('.json')]
    else:
        name = line[:-1][find_last(line[:-1], '/') + 1:line.find('.jpg')]
    jsfile=open(line[:-1])
    jsf=json.load(jsfile)
    obj=jsf['objects']
    img=cv2.imread(srcimgpath+name+'.jpg')
    if img is None:
        print srcimgpath+name+'.jpg'
        continue
    savename=name.strip()
    imgsz=[img.shape[1],img.shape[0]]
    #Size=imgsz
    #Size=[sizes,sizes]
    Size=[img.shape[1],img.shape[0]]
    MaxlightSize=150
    if Size[0]<=MaxlightSize or Size[1]<=MaxlightSize:
        continue
    #if Size[0]<img.shape[1] or Size[1]<img.shape[0]:
    #    continue
    num_row=(imgsz[0]-MaxlightSize)/(Size[0]-MaxlightSize)+1
    num_col=(imgsz[1]-MaxlightSize)/(Size[1]-MaxlightSize)+1
    for i in range(0,num_row):
        for j in range(0,num_col):
            #j=0
            imgrect=[max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])),max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])),min(Size[0],imgsz[0]),min(imgsz[1],Size[1])]
            imgcroped=img[max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])):max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1]))+min(imgsz[1],Size[1]),max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])):max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0]))+min(Size[0],imgsz[0]),:]
            if imgcroped.shape[1]!= Size[0] or imgcroped.shape[0]!= Size[1]:  
               print imgcroped.shape[1],imgcroped.shape[0] 
            #else:
            #    continue         
            num=0
            datalist=[]
            for x in obj:
                lbrect=x['rect']
                lb=x['label']
                if lb=='hei' or lb == 'hei-shu' or lb == 'hei-heng':
                    continue
                #if lbrect[2]>lbrect[3]:
                #    lb=lb+'-heng'
                #else:
                #    lb=lb+'-shu'
                #print lbrect[0],lbrect[1],lbrect[2]
                lb='trafficlight'
                x_new=float(lbrect[0])-imgrect[0]
                y_new=float(lbrect[1])-imgrect[1]
                w_new=float(lbrect[2])#-imgrect[2]
                h_new=float(lbrect[3])#-imgrect[3]
                if x_new>=-w_new*0.1 and y_new>=-h_new*0.1 and x_new+w_new<=Size[0]+w_new*0.1 and y_new+h_new<=Size[1]+h_new*0.1 and w_new>0 and h_new>0:                    
                    num=num+1
                    newlist=[lb,str(max(0,int(x_new))),str(max(0,int(y_new))),str(min(imgcroped.shape[1],int(x_new+w_new))),str(min(imgcroped.shape[0],int(y_new+h_new)))]
                    datalist.append(newlist)
            if len(datalist)>0:    
                savetxt=open(savelabelpath+savename+'_'+str(sizes)+'_'+str(i)+'_'+str(j)+'.txt','w') 
                savetxt.write(str(imgcroped.shape[1])+' '+str(imgcroped.shape[0])+'\n')
                savetxt.write(str(num)+'\n')
                for t in datalist:
                    savetxt.write(t[0]+' '+t[1]+' '+t[2]+' '+t[3]+' '+t[4]+'\n')
                cv2.imwrite(saveimgpath+savename+'_'+str(sizes)+'_'+str(i)+'_'+str(j)+'.jpg',imgcroped)