#coding=utf-8
import os
import shutil




def creatlist(srcpath,savelist):
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
        return

if __name__ =='__main__':
    srcpath='/data_1/weizhang/data/越过停止线判断/data/all/train'
    savelist='/data_1/weizhang/data/越过停止线判断/data/all/train.txt'
    creatlist(srcpath,savelist)