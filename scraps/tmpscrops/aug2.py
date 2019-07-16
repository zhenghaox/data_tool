# -*- coding: utf-8 -*-
import os
import random
from imgaug import augmenters as iaa
import cv2

import shutil

if __name__ == '__main__':
    src_imgpath = '/data_1/weizhang/data/红绿灯分类测试/0711/data/train'
    out_imgpath = '/data_1/weizhang/data/红绿灯分类测试/0711/data/train_aug_2'
    list=os.listdir(src_imgpath)
    seq = iaa.Sequential([
        iaa.Affine(rotate=(3, 8))
        
    ])
    for label in list:
        imgpath=os.path.join(src_imgpath,label)
        imgoutpath=os.path.join(out_imgpath,label)
        print imgoutpath
        if not os.path.exists(imgoutpath):
            os.mkdir(imgoutpath)
        imgnames=os.listdir(imgpath)
        for imgname in imgnames:
            imgpathname=os.path.join(imgpath,imgname)
            outimgpathname=os.path.join(imgoutpath,imgname)

            img=cv2.imread(imgpathname)
            img_aug = seq.augment_image(img)
            cv2.imwrite(outimgpathname,img_aug)

        #img=cv2.imread(imgpath)
