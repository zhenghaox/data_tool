#coding=utf-8
import os
import shutil




def creatlist():
        srcpath='/data_1/weizhang/data/红绿灯分类测试/0711/data/train_aug_2'
        savelist='/data_1/weizhang/data/红绿灯分类测试/0711/data/train_aug_2.list'
        f=open(savelist,'w')
        filelist=os.listdir(srcpath)
        for line in filelist:
                path=os.path.join(srcpath,line)
                imgs=os.listdir(path)
                for img in imgs:
                        saveimgpath=os.path.join(path,img)
                        f.write(saveimgpath+' '+line+'\n')
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
