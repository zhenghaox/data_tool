#coding=utf-8
import os

srctxt='/media/e/weizhang/data/QHD/0904/redlight_processing/img_plate.txt'
imglist='/media/e/weizhang/data/QHD/0904/redlight_processing/img'
cplist='/media/e/weizhang/data/QHD/0904/redlight_processing/cp'
jslist='/media/e/weizhang/data/QHD/0904/redlight_processing/js'
fimg=open(imglist,'w')
fcp=open(cplist,'w')
fjs=open(jslist,'w')
with open(srctxt) as srclist:
    lines=srclist.readlines()
for line in lines:
    words=line[:-1].split(' ')
    print line
    fimg.write('/media/e/weizhang/data/QHD/0904/redlight_processing/1625/'+words[0]+'/'+words[1]+'\n')
    fcp.write(words[2]+'\n')
    fjs.write(words[0]+'\n')
    