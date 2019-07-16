#coding=utf-8
import os
import shutil

if __name__=='__main__':
    xmlpath='/data_1/weizhang/data/铭牌文件检测/data/xml'
    imgpath='/data_1/weizhang/data/铭牌文件检测/data/mark'
    listtxt='/data_1/weizhang/data/铭牌文件检测/data/list.txt'
    f=open(listtxt,'w')
    xmllist=os.listdir(xmlpath)
    for xmlname in xmllist:
        imgname=xmlname.replace('.xml','.jpg')
        imgfilepath=os.path.join(imgpath,imgname)
        if os.path.exists(imgfilepath):
            f.write('mark/'+imgname+' '+'xml/'+xmlname+'\n')
    f.close
