#coding=utf-8
import shutil
import os
import random

if __name__ == "__main__":
    srcpath='/data_1/weizhang/data/越过停止线判断/data/0910/train'
    outpath='/data_1/weizhang/data/越过停止线判断/data/0910/test'
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    lines=os.listdir(srcpath)
    for line in lines:
        path=os.path.join(srcpath,line)
        outpath1=os.path.join(outpath,line)
        if not os.path.exists(outpath1):
            os.mkdir(outpath1)
        files=os.listdir(path)
        for file in files:
            if random.random()>0.9:
                filepath=os.path.join(path,file)
                outfilepath=os.path.join(outpath1,file)
                shutil.move(filepath,outfilepath)