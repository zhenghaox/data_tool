# coding:utf-8
import cv2
import numpy as np
img_path='/data_1/weizhang/data/红绿灯分类测试/0711/data/train_aug_2.list'
#word={}
with open(img_path) as f:
    lines=f.readlines()
for line in lines:
    word=line.split()
    src_img = cv2.imread(word[0])
    if src_img is None:
        continue
    src_h, src_w, src_c = src_img.shape
    if src_h == src_w:
        continue
    print word[0]
    dst_w = max(src_h,src_w)
    dst_img = np.zeros((dst_w, dst_w,3),dtype=np.uint8)
    src_center_x = src_w*0.5
    src_center_y = src_h*0.5 #- src_h*0.1
    dst_center_x = dst_w*0.5
    dst_center_y = dst_w*0.5
    offset_x = int(dst_center_x - src_center_x)
    offset_y = int(dst_center_y - src_center_y)
    if src_h>src_w:
        dst_img[:, offset_x:offset_x+src_w, :] = src_img
    else:
        dst_img[offset_y:offset_y+src_h, :, :] = src_img
    cv2.imwrite(word[0],dst_img)
    input = dst_img
    print input.shape
    img_h = input.shape[0]
    img_w = input.shape[1]
