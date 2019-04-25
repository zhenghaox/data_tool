#coding=utf-8
import os
import shutil

srcpath='/data_1/weizhang/data/安全带打电话/安全带/train'
savelist='/data_1/weizhang/data/安全带打电话/安全带/train.list'

f=open(savelist,'w')
filelist=os.listdir(srcpath)
num=0
for line in filelist:
    path=os.path.join(srcpath,line)
    imgs=os.listdir(path)
    for img in imgs:
        saveimgpath=os.path.join(path,img)
        f.write(saveimgpath+' '+str(num)+'\n')
    num=num+1