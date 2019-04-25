#coding=utf-8
import os
import shutil

srcpath='/data_1/weizhang/data/安全带打电话/安全带/test'
savelist='/data_1/weizhang/data/安全带打电话/安全带/test.list'

f=open(savelist,'w')
filelist=os.listdir(srcpath)

for line in filelist:
    path=os.path.join(srcpath,line)
    imgs=os.listdir(path)
    for img in imgs:
        saveimgpath=os.path.join(path,img)
        f.write(saveimgpath+' '+line+'\n')
