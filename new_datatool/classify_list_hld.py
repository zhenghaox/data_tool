#coding=utf-8
import os
import shutil
import cv2
import numpy as np


def creatlist():
        srcpath='/data_1/weizhang/data/all/后加/违法_红绿灯_20190902-OK-已检查/新建文件夹/result/all/classify'
        savelist='/data_1/weizhang/data/all/后加/违法_红绿灯_20190902-OK-已检查/新建文件夹/result/all/classify.txt'
        f=open(savelist,'w')
        filelist=os.listdir(srcpath)
        for line in filelist:
                path=os.path.join(srcpath,line)
                imgs=os.listdir(path)
                for img in imgs:
                        saveimgpath=os.path.join(path,img)
                        f.write(saveimgpath+' '+line+'\n')

                        src_img = cv2.imread(saveimgpath)
                        if src_img is None:
                                continue
                        src_h, src_w, src_c = src_img.shape
                        if src_h == src_w:
                                continue
                        print saveimgpath
                        dst_w = max(src_h,src_w)
                        dst_img = np.zeros((dst_w, dst_w,3),dtype=np.uint8)
                        src_center_x = src_w*0.5
                        src_center_y = src_h*0.5 
                        dst_center_x = dst_w*0.5
                        dst_center_y = dst_w*0.5
                        offset_x = int(dst_center_x - src_center_x)
                        offset_y = int(dst_center_y - src_center_y)
                        if src_h>src_w:
                                dst_img[:, offset_x:offset_x+src_w, :] = src_img
                        else:
                                dst_img[offset_y:offset_y+src_h, :, :] = src_img
                        cv2.imwrite(saveimgpath,dst_img)
                        input = dst_img
                        print input.shape
                        img_h = input.shape[0]
                        img_w = input.shape[1]
        return

def creatlist2():
        srcpath='/data_1/weizhang/data/红绿灯分类测试/0711/error'
        savelist='/data_1/weizhang/data/红绿灯分类测试/0711/error.list'
        f=open(savelist,'w')
        filelist=os.listdir(srcpath)
        for line in filelist:
                path=os.path.join(srcpath,line)
                imgs=os.listdir(path)
                for img in imgs:
                        index=img.find('_')
                        img1=img[index+1:]
                        f.write(img1+' '+line+'\n')
        return

def find_and_fix():
        ori_txt='/data_1/weizhang/data/classify/测试/0705_1/val.txt'
        new_txt='/data_1/weizhang/data/classify/测试/0705_1/val_new.txt'
        error_list='/data_1/weizhang/data/红绿灯分类测试/0711/error.list'
        f1=open(ori_txt)
        f2=open(new_txt,'w')
        f3=open(error_list)
        lines=f1.readlines()
        elines=f3.readlines()
        for line in lines:
                words=line.split(' ')
                imgpath=words[0]
                label=words[1]
                imgname=imgpath.split('/')[-1]
                errorflag=False
                #print imgname
                for eline in elines:
                        ewords=eline.split(' ')
                        eimgpath=ewords[0]
                        elabel=ewords[1]
                        if imgname==eimgpath:
                                if elabel!='99\n':
                                        f2.write(imgpath+' '+elabel)
                                        errorflag=True
                                        break
                                else:
                                        errorflag=True
                                        break
                if errorflag==False:
                        f2.write(line)


if __name__ =='__main__':
        creatlist()
        #creatlist2()
        #find_and_fix()
