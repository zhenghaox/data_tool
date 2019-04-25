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


outoripath='/media/e/weizhang/data/QHD/0720/data/outori/'
outpath='/media/e/weizhang/data/QHD/0720/data/6023out/'
savetxt='/media/e/weizhang/data/QHD/0720/data/违反导向.txt'
srcpath='/media/e/weizhang/data/QHD/0720/data/inputori/'
path='/media/e/weizhang/data/QHD/0720/data/6023/'
with open('/media/e/weizhang/data/QHD/0720/data/6023.txt') as jslist:
    lines=jslist.readlines()
f=open(savetxt,'w')
for line in lines:
    words=line.split(' ')
    print line
    #print words[0],words[1],words[2],words[3]
    name = words[4][:-1][find_last(words[4][:-1], '/') + 1:-4]
    if os.path.exists(srcpath+name+'.jpg'):
        shutil.copy(srcpath+name+'.jpg',path+name+'.jpg')
        shutil.copy(outoripath+words[0]+'.jpg',outpath+words[0]+'.jpg')
        f.write(name+'.jpg'+' '+words[1]+' '+words[0]+'.jpg'+' '+words[2]+'\n')
    #print name   
    #img=cv2.imread(srcpath+name+'.jpg')
    #print srcpath+line[:-1]
    #img=cv2.imread(line[:-1])
    #cv2.imwrite(path+name+'.jpg',img)