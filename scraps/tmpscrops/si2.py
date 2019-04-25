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


#outoripath='/media/e/weizhang/data/QHD/0725/20180725/25-html/outputData/data_1/'
#saveoutimgpath='/media/e/weizhang/data/QHD/0725/20180725/allout/'
srcpath='/media/e/weizhang/data/QHD/0727/20180726QHD/0726_25_html/inputData/'
saveimgpath='/media/e/weizhang/data/QHD/0727/20180726QHD/6023/'
savetxt='/media/e/weizhang/data/QHD/0727/20180726QHD/闯红灯.txt'
saveimgtxt='/media/e/weizhang/data/QHD/0727/20180726QHD/6023img.txt'
savecptxt='/media/e/weizhang/data/QHD/0727/20180726QHD/6023cp.txt'

if not os.path.exists(saveimgpath[:-1]):
    os.mkdir(saveimgpath[:-1])
with open('/media/e/weizhang/data/QHD/0727/20180726QHD/6023.txt') as jslist:
    lines=jslist.readlines()
f=open(savetxt,'w')
fimg=open(saveimgtxt,'w')
fcp=open(savecptxt,'w')

for line in lines:
    words=line.split(' ')
    #print line
    #print words[0],words[1],words[2],words[3]
    name = words[5][:-1][find_last(words[5][:-1], '/') + 1:-4]
    print name
    if words[4]=='3':
        if os.path.exists(srcpath+'pinjie/'+name+'.jpg'):
            shutil.copy(srcpath+'pinjie/'+name+'.jpg',saveimgpath+name+'.jpg')
            #shutil.copy(outoripath+words[0]+'.jpg',saveoutimgpath+words[0]+'.jpg')
            f.write(name+'.jpg'+' '+words[1]+' '+words[0]+'.jpg'+' '+words[2]+'\n')
            fimg.write(saveimgpath+name+'.jpg'+'\n')
            fcp.write(words[1]+'\n')
    else :
        if os.path.exists(srcpath+name+'.jpg'):
            shutil.copy(srcpath+name+'.jpg',saveimgpath+name+'.jpg')
            #shutil.copy(outoripath+words[0]+'.jpg',saveoutimgpath+words[0]+'.jpg')
            f.write(name+'.jpg'+' '+words[1]+' '+words[0]+'.jpg'+' '+words[2]+'\n') 
            fimg.write(saveimgpath+name+'.jpg'+'\n')
            fcp.write(words[1]+'\n')
    #print name   
    #img=cv2.imread(srcpath+name+'.jpg')
    #print srcpath+line[:-1]
    #img=cv2.imread(line[:-1])
    #cv2.imwrite(path+name+'.jpg',img)