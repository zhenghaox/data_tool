#coding=utf-8
import os
import cv2

passimg=open('/media/e/0531suzhou_data/16252闯红灯/passimg.txt','w')
passpl=open('/media/e/0531suzhou_data/16252闯红灯/passpl.txt','w')
cancelimg=open('/media/e/0531suzhou_data/16252闯红灯/cancelimg.txt','w')
cancelpl=open('/media/e/0531suzhou_data/16252闯红灯/cancelpl.txt','w')
passimgpath='/media/e/0531suzhou_data/16252闯红灯/通过/'
cancelimgpath='/media/e/0531suzhou_data/16252闯红灯/作废/'
with open('/media/e/0531suzhou_data/16252闯红灯/img_chepai.txt') as f:
    lines=f.readlines()
for line in lines:
    word=line.split()
    print word[0]
    img1=cv2.imread(passimgpath+word[0])
    if img1 is  None:
        continue
    passimg.write(passimgpath+word[0]+'\n')
    passpl.write(word[1]+'\n')

for line2 in lines:
    word2=line2.split()
    img2=cv2.imread(cancelimgpath+word2[0])
    if img2 is  None:
        continue
    cancelimg.write(cancelimgpath+word2[0]+'\n')
    cancelpl.write(word2[1]+'\n')