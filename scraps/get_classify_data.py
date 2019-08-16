#coding=utf-8
import os
import cv2
import json
import random

randownum=3
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

path='/data_1/weizhang/data/all/后加/0807/all/classify'
srcimgpath='/data_1/weizhang/data/all/后加/0807/all/mark'
jspath='/data_1/weizhang/data/all/后加/0807/all/json'
lines=os.listdir(jspath)
# with open('/data_1/weizhang/data/义乌/0122/jslist') as jslist:
#     lines=jslist.readlines()
for line in lines:
    ww=line.split('/')
    name = ww[-1][:ww[-1].find('.')]
    jsfile=open(jspath+'/'+line)
    jsf=json.load(jsfile)
    obj=jsf['objects']
    print srcimgpath+'/'+name+'.jpg'
    img=cv2.imread(srcimgpath+'/'+name+'.jpg')
    if img is None:
        continue
    imgsz=[img.shape[1],img.shape[0]]
    num=0

    if not os.path.exists(path+'/0/'):
        os.mkdir(path+'/0/')
    if not os.path.exists(path+'/1/'):
        os.mkdir(path+'/1/')
    if not os.path.exists(path+'/2/'):
        os.mkdir(path+'/2/')
    if not os.path.exists(path+'/3/'):
        os.mkdir(path+'/3/')
    if not os.path.exists(path+'/4/'):
        os.mkdir(path+'/4/')
    if not os.path.exists(path+'/5/'):
        os.mkdir(path+'/5/')
    if not os.path.exists(path+'/6/'):
        os.mkdir(path+'/6/')
    if not os.path.exists(path+'/7/'):
        os.mkdir(path+'/7/')
    if not os.path.exists(path+'/8/'):
        os.mkdir(path+'/8/')
    if not os.path.exists(path+'/9/'):
        os.mkdir(path+'/9/')
    if not os.path.exists(path+'/11/'):
        os.mkdir(path+'/11/')

    for x in obj:
        num=num+1
        lbrect=x['rect']
        dx1=lbrect[2]*(random.random()-0.5)*0.4
        dy1=lbrect[3]*(random.random()-0.5)*0.4
        dx2=lbrect[2]*(random.random()-0.5)*0.4
        dy2=lbrect[3]*(random.random()-0.5)*0.4
        xmin=max(lbrect[0]+dx1,0)
        xmax=min(lbrect[0]+lbrect[2]+dx2,imgsz[0])
        ymin=max(lbrect[1]+dy1,0)
        ymax=min(lbrect[1]+lbrect[3]+dy2,imgsz[1])
        img2=img[int(ymin):int(ymax),int(xmin):int(xmax),:]
        lb=x['label']
        if lb=='hong-zhi':
            cv2.imwrite(path+'/2/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='hong-zuo':
        
            cv2.imwrite(path+'/3/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='hong-you':
        
            cv2.imwrite(path+'/1/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='huang-zhi':
        
            cv2.imwrite(path+'/5/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='huang-zuo':
        
            cv2.imwrite(path+'/6/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='huang-you':
        
            cv2.imwrite(path+'/4/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='lv-zhi':
        
            cv2.imwrite(path+'/8/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='lv-zuo':
        
            cv2.imwrite(path+'/9/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='lv-you':
        
            cv2.imwrite(path+'/7/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        if lb=='hei':
        
            cv2.imwrite(path+'/0/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        if lb=='feijidongchedeng':
        
            cv2.imwrite(path+'/11/'+name+'_'+str(num)+'_'+str(randownum)+'_'+'.jpg',img2)
        
        
        
       