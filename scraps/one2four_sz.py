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
#src_path='/data_1/weizhang/data/义乌/20190128/pj'
src_path='/data_1/weizhang/data/红绿灯标注/0813/select'
imgpath='/data_1/weizhang/data/红绿灯标注/0813/select2'
lines=os.listdir(src_path)
for line in lines:
        name = line[:-1][find_last(line[:-1], '/') + 1:-3]
        imgpaths=os.path.join(src_path,line)
        img=cv2.imread(imgpaths)
        if img is None:
            print imgpaths
            continue
        imgsz=[img.shape[1],img.shape[0]]

        img1=img[:imgsz[1]/2,:imgsz[0]/2,:]
        img2=img[:imgsz[1]/2,imgsz[0]/2:,:]
        img3=img[imgsz[1]/2:,:imgsz[0]/2,:]
        img4=img[imgsz[1]/2:,imgsz[0]/2:,:]

        #cv2.imwrite(path+name+'_1.jpg',img1)
        cv2.imwrite(imgpath+'/'+name+'_2.jpg',img2)
       # cv2.imwrite(path+name+'_3.jpg',img3)
        #cv2.imwrite(path+name+'_4.jpg',img4)