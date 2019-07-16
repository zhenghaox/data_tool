#coding=utf-8
import shutil
import os

filelist=[]

def list_all_files(now_dir):  
    if os.path.isfile(now_dir):  
        filelist.append(now_dir)
    else:  
        listdir = os.listdir(now_dir)  
        for i in listdir:  
            if not os.path.isfile(i):     
                i = now_dir + '/' + i  
                list_all_files(i)  

if __name__ == '__main__':
    src_path='/run/user/1000/gvfs/smb-share:server=192.168.30.41,share=shenruixue_up/031.违法数据差异数据完成/枣庄/闯红灯-ok'
    out_path='/data_1/weizhang/data/renane/枣庄/闯红灯_ok'
    list_all_files(src_path)
    for file in filelist:
        file = file.strip('\n')
        filename=file.split('/')[-1]
        wordsss=filename[filename.find('_')+1:]
        outfile1=file.replace(src_path,out_path)
        outfile=outfile1.replace(filename,wordsss)
        print outfile
        creat_out_path='/'
        num=0
        words=outfile.split('/')
        for word in words:
            num=num+1
            if num ==len(words):
                continue
            creat_out_path=os.path.join(creat_out_path,word)
            if not os.path.exists(creat_out_path):
                os.mkdir(creat_out_path)
        filename=file.split('/')[-1]
        #wordsss=filename[filename.find('_'):]
        #print wordsss
        shutil.copy(file,outfile)
        # if filename[-4:] == '.jpg' or filename[-4:] == '.log' or filename[-5:] =='.json' or filename[-5:] =='.conf' or filename[-4:] =='.ini' or filename[-3:] =='.bk' or filename[-3:] =='.gz' or filename[-4:] =='.txt' :
        #     shutil.copy(file,outfile)
        # elif filename == 'yolov3.weights' or filename =='yolov3.cfg':
        #     shutil.copy(file,outfile)
        # else:
        #     cmd='cd '+run_path+' \n ./e key iv '+file+' '+outfile
        #     os.system(cmd)
        