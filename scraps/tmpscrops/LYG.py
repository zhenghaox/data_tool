#coding=utf-8
import os
import cv2
import shutil
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


srcpath='/media/e/weizhang/data/LYG/processed/'
saveimgpath='/media/e/weizhang/data/LYG/process0926/'
#savetxt='/media/e/weizhang/data/QHD/0727/20180726QHD/闯红灯.txt'
#saveimgtxt='/media/e/weizhang/data/QHD/0727/20180726QHD/6023img.txt'
#savecptxt='/media/e/weizhang/data/QHD/0727/20180726QHD/6023cp.txt'

if not os.path.exists(saveimgpath[:-1]):
    os.mkdir(saveimgpath[:-1])
with open('/media/e/weizhang/data/LYG/0613-0630.csv') as jslist:
    lines=jslist.readlines()
#f=open(savetxt,'w')
#fimg=open(saveimgtxt,'w')
#fcp=open(savecptxt,'w')
num=0
imgnum1=0
imgnum2=0
imgnum3=0
for line in lines:
    num=num+1
    if num == 1:
        continue
    words=line.split(',')
    camreid = words[6][1:-1]
    wflx = words[5][1:-1]
    tg=words[13][1:-1]
    date=words[4][1:-1].split(' ')[0].split('/')[0]+words[4][1:-1].split(' ')[0].split('/')[1]+words[4][1:-1].split(' ')[0].split('/')[2]
    img1=words[14].split('/')[-1][:-1]
    img2=words[15].split('/')[-1][:-1]
    img3=words[16].split('/')[-1][:-1]
    list_t=os.path.join(srcpath,wflx)
    list=os.path.join(list_t,tg)
    #print list
    

    savepath1=os.path.join(saveimgpath,wflx)
    if  not os.path.exists(savepath1):
            os.mkdir(savepath1)
    savepath2=os.path.join(savepath1,camreid)
    if  not os.path.exists(savepath2):
            os.mkdir(savepath2)
    
    if len(img1) >1:
        img1p=os.path.join(list,img1)
        if os.path.exists(img1p):
            shutil.copy(img1p,savepath2+'/'+words[2][1:-1]+'@'+date+'@'+words[0][1:-1]+'@0.jpg')
        else:
            imgnum1=imgnum1+1
            print img1
    else:
        imgnum1=imgnum1+1
        print img1
    if len(img2) >1:
        img2p=os.path.join(list,img2)
        if os.path.exists(img2p):
            shutil.copy(img2p,savepath2+'/'+words[2][1:-1]+'@'+date+'@'+words[0][1:-1]+'@1.jpg')
        else:
            imgnum2=imgnum2+1
            print img2
    else:
            imgnum2=imgnum2+1
            print img2
    if len(img3) >1:
        img3p=os.path.join(list,img3)
        if os.path.exists(img3p):
            shutil.copy(img3p,savepath2+'/'+words[2][1:-1]+'@'+date+'@'+words[0][1:-1]+'@2.jpg')
        else:
            imgnum3=imgnum3+1
            print img3
    else:
        imgnum3=imgnum3+1
        #print img3
    #print str(imgnum1)+' '+str(imgnum2)+' '+str(imgnum3)        
    #print savepath2
print str(imgnum1)+' '+str(imgnum2)+' '+str(imgnum3)