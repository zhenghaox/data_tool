#coding=utf-8
import os
import cv2
import numpy as np
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position
#srcpath='/media/e/weizhang/test/BD/AgainstRedLight/0712/cancel/'
#path='/media/e/weizhang/test/BD/AgainstRedLight/0712/cancelselect/'
f0='/data_1/weizhang/data/盐城/1112/pj/img_plate0'
f1='/data_1/weizhang/data/盐城/1112/pj/img_plate1'
f2='/data_1/weizhang/data/盐城/1112/pj/img_plate2'

fi0=open(f0,'w')
fi1=open(f1,'w')
fi2=open(f2,'w')
with open('/data_1/weizhang/170/盐城/20181108/preprocess/123') as jslist:
    lines=jslist.readlines()
for line in lines:
    #print line
    words=line[:-1].split(' ')
    cp=words[0]
    #print cp
    img1_name=words[1]
    print img1_name
    img2_name=words[2]
    img3_name=words[3]
    name1 = img1_name[find_last(img1_name[:-1], '/') + 1:-4]
    name2 = img2_name[find_last(img2_name[:-1], '/') + 1:-4]
    name3 = img3_name[find_last(img3_name[:-1], '/') + 1:-4]
    #print name3 
    img_3=cv2.imread(img1_name)
    img_4_1=cv2.imread(img2_name)
    img_5_1=cv2.imread(img3_name)
    #img_black = np.zeros((img_4.shape[0], img_5.shape[1], 3), dtype='uint8')
    if img_4_1 is None:    
        cv2.imwrite('/data_1/weizhang/data/盐城/1112/pj/0/'+name1+'.jpg',img_3)
        fi0.write('/data_1/weizhang/data/盐城/1112/pj/0/'+name1+'.jpg'+' '+cp+'\n')
    elif img_5_1 is None:
        height,width = img_3.shape[:2]
        img_4=cv2.resize(img_4_1,(width,height))
        img_5 = np.zeros((img_4.shape[0], img_4.shape[1], 3), dtype='uint8')
        img_black = np.zeros((img_4.shape[0], img_4.shape[1], 3), dtype='uint8')
        img_1 = np.concatenate([img_3, img_4], axis=1)
        img_2 = np.concatenate([img_5, img_black], axis=1)
        img = np.concatenate([img_1, img_2])
        cv2.imwrite('/data_1/weizhang/data/盐城/1112/pj/1/'+name1+'.jpg',img)
        fi1.write('/data_1/weizhang/data/盐城/1112/pj/1/'+name1+'.jpg'+' '+cp+'\n')
    else:
        height,width = img_3.shape[:2]
        img_4=cv2.resize(img_4_1,(width,height))
        img_5 = cv2.resize(img_5_1,(width,height))
        img_black = np.zeros((img_4.shape[0], img_4.shape[1], 3), dtype='uint8')
        img_1 = np.concatenate([img_3, img_4], axis=1)
        img_2 = np.concatenate([img_5, img_black], axis=1)
        img = np.concatenate([img_1, img_2])
        #cv2.imshow('test',img)
        #cv2.waitKey(0)
        cv2.imwrite('/data_1/weizhang/data/盐城/1112/pj/2/'+name1+'.jpg',img)
        fi2.write('/data_1/weizhang/data/盐城/1112/pj/2/'+name1+'.jpg'+' '+cp+'\n')
    #print srcpath+line[:-1]
    #img=cv2.imread(line[:-1])
    #cv2.imwrite(path+name+'.jpg',img)