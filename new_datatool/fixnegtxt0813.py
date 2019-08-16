#coding=utf-8
import shutil
import os

if __name__ == "__main__":
    srcpath='/data_1/weizhang/data/all/ori/neg/label'
    outpath='/data_1/weizhang/data/all/ori/neg/test'
    errpath='/data_1/weizhang/data/all/ori/neg/fixedtxt'
    if not os.path.exists(outpath):
        os.mkdir(outpath)
    if not os.path.exists(errpath):
        os.mkdir(errpath)
    lines=os.listdir(srcpath)
    for line in lines:
        txtpath=os.path.join(srcpath,line)
        txtlines=open(txtpath)
        outtxtpath=os.path.join(outpath,line)
        errtxtpath=os.path.join(errpath,line)
        f=open(outtxtpath,'w')
        num=0
        negnum=0
        for txtline in txtlines:
            datas=txtline.split(' ')
            if len(datas)==5:
                if datas[1]>=datas[3] or datas[2] >=datas[4]:
                    negnum=negnum+1
                    continue
                f.write('1'+' '+datas[1]+' '+datas[2]+' '+datas[3]+' '+datas[4])
                num=num+1
        f.close
        if num==0:
            shutil.move(outtxtpath,errpath)
