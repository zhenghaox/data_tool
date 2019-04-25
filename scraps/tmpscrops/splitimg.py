#coding=utf-8
import os
import cv2
import shutil
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

with open('/media/e/weizhang/data/baoding/yxtc/script/all.txt') as flist:
    lines=flist.readlines()

for line in lines:
    #words=line.split(' ')
    name =line[find_last(line, '/') + 1:-4]
    print name
    lx=name[find_last(name, '@') + 1:-1]
    print lx

    if lx == '1':
        shutil.copy(line[:-1],'/media/e/weizhang/data/baoding/yxtc/script/yxtc/1/'+name+'.jpg')
    if lx == '2':
        shutil.copy(line[:-1],'/media/e/weizhang/data/baoding/yxtc/script/yxtc/2/'+name+'.jpg')
    if lx == '3':
        shutil.copy(line[:-1],'/media/e/weizhang/data/baoding/yxtc/script/yxtc/3/'+name+'.jpg')
    if lx == '4':
        shutil.copy(line[:-1],'/media/e/weizhang/data/baoding/yxtc/script/yxtc/4/'+name+'.jpg')
    # if words[4]=='3':
    #     if os.path.exists(srcpath+name+'.jpg'):
    #         shutil.copy(srcpath+'pinjie/'+name+'.jpg',saveimgpath+name+'.jpg')
    #         #shutil.copy(outoripath+words[0]+'.jpg',saveoutimgpath+words[0]+'.jpg')
    #         f.write(name+'.jpg'+' '+words[1]+' '+words[0]+'.jpg'+' '+words[2]+'\n')
    #         fimg.write(saveimgpath+name+'.jpg'+'\n')
    #         fcp.write(words[1]+'\n')
    # else :
    #     if os.path.exists(srcpath+name+'.jpg'):
    #         shutil.copy(srcpath+name+'.jpg',saveimgpath+name+'.jpg')
    #         #shutil.copy(outoripath+words[0]+'.jpg',saveoutimgpath+words[0]+'.jpg')
    #         f.write(name+'.jpg'+' '+words[1]+' '+words[0]+'.jpg'+' '+words[2]+'\n') 
    #         fimg.write(saveimgpath+name+'.jpg'+'\n')
    #         fcp.write(words[1]+'\n')
    #print name   
    #img=cv2.imread(srcpath+name+'.jpg')
    #print srcpath+line[:-1]
    #img=cv2.imread(line[:-1])
    #cv2.imwrite(path+name+'.jpg',img)