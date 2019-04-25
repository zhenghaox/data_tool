# -*- coding: utf-8 -*-
import os
import random
from imgaug import augmenters as iaa
import cv2

import shutil

if __name__ == '__main__':
    src_imgpath = '/data_1/weizhang/data/SZ/20190102/闯红灯/classifytest/error/10'
    list=os.listdir(src_imgpath)
    # for imglist in list:
    #     print imglist
    seq = iaa.Sequential([
        iaa.Crop(px=(0, 16),keep_size=False), # crop images from each side by 0 to 16px (randomly chosen)
        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
        iaa.Multiply((0.8, 1.2), per_channel=0.2),
        #iaa.Multiply((0.8, 1.2)),
        iaa.Sharpen(alpha=0.5),
        iaa.GaussianBlur(sigma=(0.0, 3.0)),
        #iaa.Superpixels(p_replace=0.5, n_segments=64),
        iaa.Sometimes(
            0.5,
            iaa.AdditiveGaussianNoise(scale=0.2*255),
            iaa.Add(50, per_channel=True)
                       
        ),
        #iaa.WithChannels(0, iaa.Affine(rotate=(0, 45))),
        #iaa.WithChannels(0, iaa.Add((10, 100))),
        # iaa.WithColorspace(
        #     to_colorspace="HSV",
        #     from_colorspace="RGB",
        #     children=iaa.WithChannels(0, iaa.Add((10, 50)))
        # ),
        #iaa.Fliplr(0.5), # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 3.0)) # blur images with a sigma of 0 to 3.0
    ])
    for imglist in list:
        num=0
        imgpath=os.path.join(src_imgpath,imglist)
        img=cv2.imread(imgpath)
        for batch_idx in range(5):
            num=num+1
            name_new=imglist[:-4]+'_aug_'+str(num)+'.jpg'
            outimgpath=os.path.join(src_imgpath,name_new)
            print outimgpath
            images_aug = seq.augment_image(img)
            cv2.imwrite(outimgpath,images_aug)
