#coding=utf-8
import shutil
import os
if __name__ == '__main__':
    f1=open('/data_1/weizhang/configfile/秦皇岛/list')
    f2=open('/data_2/work/weizhang/share/config/秦皇岛.txt')
    #fimg=open('/media/e/weizhang/data/QHD/0808/jiaojingori/img.txt','w')
    #fcp=open('/media/e/weizhang/data/QHD/0808/jiaojingori/plate.txt','w')
    lines1=f1.readlines()
    lines2=f2.readlines()
    for line1 in lines1:
        index=names=line1.split('/')[-1].find('.')
        names=line1.split('/')[-1][:index]
        #print names
        for line2 in lines2:
            name2=line2.split(' ')[0]
            print line2.split(' ')[1]
            #name=line2.split(' ')[2][:-1]   
            name=line2.split(' ')[1]         
            if names == name2:
                #names2=name[5].split('/')[-1][:-5]
                if os.path.exists('/data_1/weizhang/configfile/秦皇岛/130300/'+names+'.json'):
                    shutil.copy('/data_1/weizhang/configfile/秦皇岛/130300/'+names+'.json','/data_1/weizhang/configfile/秦皇岛/130300_cn/'+name+'.json')
                    #fimg.write('/media/e/weizhang/data/QHD/0808/jiaojingori/img/'+names2+'.jpg'+'\n')
                    #fcp.write(name[1]+'\n')