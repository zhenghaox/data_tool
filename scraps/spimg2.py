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

path='/data_1/weizhang/data/红绿灯标注/done/违法_红绿灯_20190604_part1/classify'
srcimgpath='/data_1/weizhang/data/红绿灯标注/done/违法_红绿灯_20190604_part1/mark'
jspath='/data_1/weizhang/data/红绿灯标注/done/违法_红绿灯_20190604_part1/json'
lines=os.listdir(jspath)
# with open('/data_1/weizhang/data/义乌/330700000000330782000115020002/result/123/jslist') as jslist:
#     lines=jslist.readlines()
for line in lines:
    ww=line.split('/')
    name = ww[-1][:ww[-1].find('.')]
    save_name=name.strip()
    jsfile=open(jspath+'/'+line)
    jsf=json.load(jsfile)
    obj=jsf['objects']
    print srcimgpath+'/'+name+'.jpg'
    img=cv2.imread(srcimgpath+'/'+name+'.jpg')
    if img is None:
        print 'img error!!!'
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
        lb=x['label']
        img2=img[int(lbrect[1]):int(lbrect[1])+int(lbrect[3]),int(lbrect[0]):int(lbrect[0])+int(lbrect[2]),:]
        if lb=='hong-zhi':
            cv2.imwrite(path+'/2/'+save_name+'_'+str(num)+'.jpg',img2)       
        if lb=='hong-zuo':
        
            cv2.imwrite(path+'/3/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='hong-you':
        
            cv2.imwrite(path+'/1/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='huang-zhi':
        
            cv2.imwrite(path+'/5/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='huang-zuo':
        
            cv2.imwrite(path+'/6/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='huang-you':
        
            cv2.imwrite(path+'/4/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='lv-zhi':
        
            cv2.imwrite(path+'/8/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='lv-zuo':
        
            cv2.imwrite(path+'/9/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='lv-you':
        
            cv2.imwrite(path+'/7/'+save_name+'_'+str(num)+'.jpg',img2)
        
        if lb=='hei':
        
            cv2.imwrite(path+'/0/'+save_name+'_'+str(num)+'.jpg',img2)
        if lb=='feijidongchedeng':
        
            cv2.imwrite(path+'/11/'+save_name+'_'+str(num)+'.jpg',img2)
        
        
        
       