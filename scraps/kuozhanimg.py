# coding:utf-8

#import sys.io
import os
import sys
import cv2
import numpy as np

img_path='/media/d/work/weizhang/data/classify/hongzhi/20180328061430_╝╜BH5823_0_0_27928905_1_3_2.jpg'
src_img = cv2.imread(img_path)
#src_img = cv2.cvtColor(src_img, cv2.COLOR_RGB2BGR)
#src_img = np.transpose(src_img, [1,0,2])

src_h, src_w, src_c = src_img.shape
dst_w = max(src_h,src_w)
dst_img = np.zeros((dst_w, dst_w,3),dtype=np.uint8)
src_center_x = src_w*0.5
src_center_y = src_h*0.5 - src_h*0.1
dst_center_x = dst_w*0.5
dst_center_y = dst_w*0.5
offset_x = int(dst_center_x - src_center_x)
offset_y = int(dst_center_y - src_center_y)
if src_h>src_w:
    dst_img[:, offset_x:offset_x+src_w, :] = src_img
else:
    dst_img[offset_y:offset_y+src_h, :, :] = src_img
cv2.imwrite('tmp.jpg',dst_img)
input = dst_img
print input.shape
img_h = input.shape[0]
img_w = input.shape[1]