#coding=utf-8
import os
import cv2
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

path='/media/e/weizhang/data/QHD/0808/out/select_1/'
with open('/media/e/weizhang/data/QHD/0808/out/selectlist') as jslist:
    lines=jslist.readlines()
for line in lines:
    name = line[:-1][find_last(line[:-1], '/') + 1:-4]
    #if name[-1:]!='3' and name[-1:]!='4' and name[-1:]!='5':
    img=cv2.imread(line[:-1])
    if img is None:
        print 11111
        continue
    imgsz=[img.shape[1],img.shape[0]]
    img1=img[:imgsz[1]/2+imgsz[1]/80,:imgsz[0]/2,:]
    img2=img[:imgsz[1]/2+imgsz[1]/80,imgsz[0]/2:,:]
    img3=img[imgsz[1]/2-imgsz[1]/80:,:imgsz[0]/2,:]
    img4=img[imgsz[1]/2-imgsz[1]/80:,imgsz[0]/2:,:]

    #img1=img[:imgsz[1]/2,:imgsz[0]/2,:]
    #img2=img[:imgsz[1]/2,imgsz[0]/2:,:]
    #img3=img[imgsz[1]/2:,:imgsz[0]/2,:]
    #img4=img[imgsz[1]/2-imgsz[1]/80:,imgsz[0]/2:,:]

    cv2.imwrite(path+name+'_1.jpg',img1)
    #cv2.imwrite(path+name+'_2.jpg',img2)
    #cv2.imwrite(path+name+'_3.jpg',img3)
    #cv2.imwrite(path+name+'_4.jpg',img4)