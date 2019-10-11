#coding=utf-8
import shutil
import os
if __name__ == '__main__':
    f1=open('/media/e/weizhang/data/QHD/0808/out/coflist')
    f2=open('/media/e/weizhang/data/QHD/0808/out/img_plate.txt')
    fimg=open('/media/e/weizhang/data/QHD/0808/jiaojingori/img.txt','w')
    fcp=open('/media/e/weizhang/data/QHD/0808/jiaojingori/plate.txt','w')
    lines1=f1.readlines()
    lines2=f2.readlines()
    for line1 in lines1:
        names=line1.split('/')[-1][:-5]
        #print names
        for line2 in lines2:
            name2=line2.split(' ')[0]
            name=line2.split(' ')
            #print name2
            if names == name2:
                names2=name[5].split('/')[-1][:-5]
                if os.path.exists('/media/e/weizhang/data/QHD/0808/src/'+names2+'.jpg'):
                    shutil.copy('/media/e/weizhang/data/QHD/0808/src/'+names2+'.jpg','/media/e/weizhang/data/QHD/0808/jiaojingori/img/'+names2+'.jpg')
                    fimg.write('/media/e/weizhang/data/QHD/0808/jiaojingori/img/'+names2+'.jpg'+'\n')
                    fcp.write(name[1]+'\n')
        


