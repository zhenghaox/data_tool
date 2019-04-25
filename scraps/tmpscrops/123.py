#coding=utf-8
import os
import shutil

srcpath='/media/e/car/车标分类/lenet_chebiao/train'
savelist='/media/e/car/车标分类/lenet_chebiao/label.txt'

f=open(savelist,'w')
filelist=os.listdir(srcpath)
num=0
for line in filelist:
    path=os.path.join(srcpath,line)
    imgs=os.listdir(path)
    f.write(line+' '+str(num)+'\n')
    for img in imgs:
        saveimgpath=os.path.join(path,img)
        #f.write(saveimgpath+' '+str(num)+'\n')
    num=num+1
