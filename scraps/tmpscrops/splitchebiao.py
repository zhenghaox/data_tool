#coding=utf-8
import os
import shutil

srcpath='/data_1/car/pro/detec-car-ssd/debug/re1'
savepath='/data_1/car/pro/detec-car-ssd/debug/re2'
#savelist='/data_1/weizhang/data/QHD/1201/test/erlist'

#f=open(savelist,'w')
filelist=os.listdir(srcpath)

for line in filelist:
    path=os.path.join(srcpath,line)
    #print line
    chepai=line.split('_')[0]
    path2=os.path.join(savepath,chepai)
    print path2
    if not os.path.exists(path2):
        os.mkdir(path2)
    saveimg=os.path.join(path2,line)
    shutil.copy(path,saveimg)
    #imgs=os.listdir(path)
    #for img in imgs:
    #    saveimgpath=os.path.join(path,img)
    #    f.write(saveimgpath+' '+line+'\n')