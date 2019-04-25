#coding=utf-8
import os
import shutil


if __name__ == '__main__':

    srcpath='/run/user/1000/gvfs/smb-share:server=192.168.30.41,share=xuzhenghao_up/2019/2019.4.8/cut_moved_01/result'
    savepath='/data_1/weizhang/data/安全带打电话/done/all/result'
    filelist=os.listdir(srcpath)
    for line in filelist:
        path=os.path.join(srcpath,line)
        filepaths=os.listdir(path)
        for filepath in filepaths:
            saveimgpath=os.path.join(path,filepath)
            imgs=os.listdir(saveimgpath)
            if filepath =='xml':
                for img in imgs:
                    imgpath=os.path.join(saveimgpath,img)
                    if os.path.exists(imgpath):
                        print savepath+'/xml/'+img
                        shutil.copy(imgpath,savepath+'/xml/'+img)
            if filepath =='mark':
                for img in imgs:
                    imgpath=os.path.join(saveimgpath,img)
                    if os.path.exists(imgpath):
                        shutil.copy(imgpath,savepath+'/mark/'+img)
                        print savepath+'/mark/'+img




