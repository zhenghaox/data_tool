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

saveimgpath='/data_1/weizhang/data/testssd/img/'
savelabelpath='/data_1/weizhang/data/testssd/label/'
srcimgpath='/data_1/weizhang/data/BDdone/all/img/'
with open('/data_1/weizhang/data/BDdone/all/jsonlist') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:line.find('.')]
    jsfile=open(line[:-1])
    jsf=json.load(jsfile)
    obj=jsf['objects']
    img=cv2.imread(srcimgpath+name+'.jpg')
    if img is None:
        print srcimgpath+name+'.jpg'
        continue
    imgsz=[img.shape[1],img.shape[0]]
    Size=[320,320]
    MaxlightSize=150
    num_row=(imgsz[0]-MaxlightSize)/(Size[0]-MaxlightSize)+1
    num_col=(imgsz[1]-MaxlightSize)/(Size[1]-MaxlightSize)+1
    for i in range(0,num_row):
        for j in range(0,num_col):
            #j=0
            imgrect=[max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])),max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])),min(Size[0],imgsz[0]),min(imgsz[1],Size[1])]
            imgcroped=img[max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1])):max(0,min(j*(Size[1]-MaxlightSize),imgsz[1]-Size[1]))+min(imgsz[1],Size[1]),max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0])):max(0,min(i*(Size[0]-MaxlightSize),imgsz[0]-Size[0]))+min(Size[0],imgsz[0]),:]
            if imgcroped.shape[1]!= Size[0] or imgcroped.shape[0]!= Size[1]:  
               print imgcroped.shape[1],imgcroped.shape[0]          
            num=0
            datalist=[]
            for x in obj:
                lbrect=x['rect']
                lb=x['label']
                if lbrect[2]>lbrect[3]:
                    lb=lb+'-heng'
                else:
                    lb=lb+'-shu'
                #print lbrect[0],lbrect[1],lbrect[2]
                x_new=float(lbrect[0])-imgrect[0]
                y_new=float(lbrect[1])-imgrect[1]
                w_new=float(lbrect[2])#-imgrect[2]
                h_new=float(lbrect[3])#-imgrect[3]
                if x_new>=-w_new*0.1 and y_new>=-h_new*0.1 and x_new+w_new<=Size[0]+w_new*0.1 and y_new+h_new<=Size[1]+h_new*0.1:                    
                    num=num+1
                    newlist=[lb,str(max(0,int(x_new))),str(max(0,int(y_new))),str(min(Size[0],int(x_new+w_new))),str(min(Size[1],int(y_new+h_new)))]
                    datalist.append(newlist)
                    #savetxt.write(lb+' '+str(x_new)+' '+str(y_new)+' '+str(x_new+w_new)+' '+str(y_new+h_new)+'\n')
                    #cv2.rectangle(imgcroped,(int(x_new),int(y_new)),(int(x_new+w_new),int(y_new+h_new)),(0,0,255),2)
                    #print name,i,j,x_new,y_new,w_new,h_new
            if len(datalist)>0:    
                #print num
                savetxt=open(savelabelpath+name+'_320_'+str(i)+'_'+str(j)+'.txt','w') 
                savetxt.write(str(num)+'\n')
                for t in range(0,len(datalist)):
                    #print datalist[t-1][0]
                    savetxt.write(datalist[t-1][0]+' '+datalist[t-1][1]+' '+datalist[t-1][2]+' '+datalist[t-1][3]+' '+datalist[t-1][4]+'\n')
                cv2.imwrite(saveimgpath+name+'_320_'+str(i)+'_'+str(j)+'.jpg',imgcroped)
            else:
                savetxt=open(savelabelpath+name+'_320_'+str(i)+'_'+str(j)+'.txt','w') 
                savetxt.write(str(num)+'\n')
                cv2.imwrite(saveimgpath+name+'_320_'+str(i)+'_'+str(j)+'.jpg',imgcroped)