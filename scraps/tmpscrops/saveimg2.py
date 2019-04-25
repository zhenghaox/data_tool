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


#outoripath='/media/e/weizhang/data/QHD/0720/data/outori/'
outpath='/data_2/work/weizhang/share/胡威/classify/'
#savetxt='/media/e/weizhang/data/QHD/0720/data/违反导向.txt'
#srcpath='/media/e/weizhang/data/QHD/0720/data/inputori/'
#path='/media/e/weizhang/data/QHD/0720/data/6023/'
with open('/data_2/work/weizhang/share/胡威/classify/无标题文档') as jslist:
    lines=jslist.readlines()
#f=open(savetxt,'w')
for line in lines:
    words=line.split(' ')
    #print line
    #print words[0],words[1],words[2],words[3]
    name = words[0][find_last(words[0][:-1], '/') + 1:-4]
    #print words[0]
    #print name
    lb=words[1][:-1]
    #print outpath+lb+'/'+name+'.jpg'
    #print lb
    if not os.path.exists(outpath+lb):
        os.mkdir(outpath+lb)    
    print words[0]
    if os.path.exists('/'+words[0]):
        #print words[0]
        shutil.copy('/'+words[0],outpath+lb+'/'+name+'.jpg')
        #shutil.copy(outoripath+words[0]+'.jpg',outpath+words[0]+'.jpg')
        #f.write(name+'.jpg'+' '+words[1]+' '+words[0]+'.jpg'+' '+words[2]+'\n')
    #print name   
    #img=cv2.imread(srcpath+name+'.jpg')
    #print srcpath+line[:-1]
    #img=cv2.imread(line[:-1])
    #cv2.imwrite(path+name+'.jpg',img)