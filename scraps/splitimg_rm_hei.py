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

saveimgpath='/data_1/weizhang/data/all/cut/960_img/'
savelabelpath='/data_1/weizhang/data/all/cut/960_label/'
srcimgpath='/data_1/weizhang/data/all/ori/mark/'
sizes=960
with open('/data_1/weizhang/data/all/ori/jslist') as jslist:
    lines=jslist.readlines()
for line in lines:
    name=''
    name = line[:-1][find_last(line[:-1], '/') + 1:-9]
    jsfile=open(line[:-1])
    jsf=json.load(jsfile)
    obj=jsf['objects']
    img=None
    img=cv2.imread(srcimgpath+name+'.jpg')
    if img is None:
        print srcimgpath+name+'.jpg'
        name = line[:-1][find_last(line[:-1], '/') + 1:-5]
        img=cv2.imread(srcimgpath+name+'.jpg')
        if img is None:
            print srcimgpath+name+'.jpg'
            continue
    name=name.strip()
    imgsz=[img.shape[1],img.shape[0]]
    #Size=[img.shape[1]/4,img.shape[0]/4]
    Size=[sizes,sizes]
    #print imgsz,Size
    MaxlightSize=150
    if Size[0] <=MaxlightSize or Size[1] <=MaxlightSize :
        continue
    num_row=(imgsz[0]-MaxlightSize)/(Size[0]-MaxlightSize)+1
    num_col=(imgsz[1]-MaxlightSize)/(Size[1]-MaxlightSize)+1
    for i in range(0,num_row):
        for j in range(0,num_col):
            #j=0
            imgrect=[max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])),max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])),min(Size[0],imgsz[0]),min(imgsz[1],Size[1])]
            imgcroped=img[max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])):max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1]))+min(imgsz[1],Size[1]),max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])):max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0]))+min(Size[0],imgsz[0]),:]
            if imgcroped.shape[1]!= Size[0] or imgcroped.shape[0]!= Size[1]:  
               #print imgcroped.shape[1],imgcroped.shape[0]
               pass          
            num=0
            datalist=[]
            for x in obj:
                lbrect=x['rect']
                lb=x['label']
                if lb == 'hei':
                   continue

                #if lbrect[2]>lbrect[3]:
                #    lb=lb+'-heng'
                #else:
                #    lb=lb+'-shu'
                #print lbrect[0],lbrect[1],lbrect[2]

                #################
                lb='trafficlight'
                ################
                x_new=float(lbrect[0])-imgrect[0]
                y_new=float(lbrect[1])-imgrect[1]
                w_new=float(lbrect[2])#-imgrect[2]
                h_new=float(lbrect[3])#-imgrect[3]
                if x_new>=-5 and y_new>=-5 and x_new+w_new<=imgcroped.shape[1]+5 and y_new+h_new<=imgcroped.shape[0]+5:                    
                    num=num+1
                    newlist=[lb,str(max(0,int(x_new))),str(max(0,int(y_new))),str(min(imgcroped.shape[1],int(x_new+w_new))),str(min(imgcroped.shape[0],int(y_new+h_new)))]
                    datalist.append(newlist)
                    #savetxt.write(lb+' '+str(x_new)+' '+str(y_new)+' '+str(x_new+w_new)+' '+str(y_new+h_new)+'\n')
                    #cv2.rectangle(imgcroped,(int(x_new),int(y_new)),(int(x_new+w_new),int(y_new+h_new)),(0,0,255),2)
                    #print name,i,j,x_new,y_new,w_new,h_new
            if len(datalist)>0:    
                #print num
                savetxt=open(savelabelpath+name+'_'+str(sizes)+'_'+str(i)+'_'+str(j)+'.txt','w') 
                savetxt.write(str(imgcroped.shape[1])+' '+str(imgcroped.shape[0])+'\n')
                savetxt.write(str(num)+'\n')
                for t in range(0,len(datalist)):
                    #print datalist[t-1][0]
                    savetxt.write(datalist[t-1][0]+' '+datalist[t-1][1]+' '+datalist[t-1][2]+' '+datalist[t-1][3]+' '+datalist[t-1][4]+'\n')
                cv2.imwrite(saveimgpath+name+'_'+str(sizes)+'_'+str(i)+'_'+str(j)+'.jpg',imgcroped)