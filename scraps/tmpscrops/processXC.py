#coding=utf-8
import os
import shutil

srcpath='/media/e/weizhang/data/XC'
saveimgpath='/media/e/weizhang/data/processed/'

if not os.path.exists(saveimgpath[:-1]):
    os.mkdir(saveimgpath[:-1])

filelist=os.listdir(srcpath)

for line in filelist:
    list=os.path.join(srcpath,line)
    savepath1=os.path.join(saveimgpath,line)
    if  not os.path.exists(savepath1):
            os.mkdir(savepath1)
    imgpath=os.listdir(list)
    for li in imgpath:
        name = li[:li.find('.')]
        words=li.split('@')
        savepath2=os.path.join(savepath1,words[0])
        if  not os.path.exists(savepath2):
            os.mkdir(savepath2)
        savepath3=os.path.join(savepath2,li)
        srcimg=os.path.join(list,li)
        shutil.copy(srcimg,savepath3)