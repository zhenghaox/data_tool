#coding=utf-8
import shutil
import os
if __name__ == '__main__':
    f1=open('/data_1/weizhang/data/QHD/1127/conf/list')
    lines1=f1.readlines()
    for line1 in lines1:
        index=names=line1.split('/')[-1].find('.')
        names=line1.split('/')[-1][:index]
        if os.path.exists('/data_1/weizhang/data/QHD/1127/conf/json/'+names+'.jpg.json'):
            shutil.copy('/data_1/weizhang/data/QHD/1127/conf/json/'+names+'.jpg.json','/data_1/weizhang/data/QHD/1127/conf/320300_old/'+names+'.json')               