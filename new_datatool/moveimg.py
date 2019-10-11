#coding=utf-8
import shutil
import os

filelist=[]
orilist=[]

def list_all_files(now_dir):  
    if os.path.isfile(now_dir):  
        filelist.append(now_dir)
    else:  
        listdir = os.listdir(now_dir)  
        for i in listdir:  
            if not os.path.isfile(i):     
                i = now_dir + '/' + i  
                list_all_files(i)  

def list_all_files2(now_dir):  
    if os.path.isfile(now_dir):  
        orilist.append(now_dir)
    else:  
        listdir = os.listdir(now_dir)  
        for i in listdir:  
            if not os.path.isfile(i):     
                i = now_dir + '/' + i  
                list_all_files2(i)  

if __name__ == '__main__':
    ori_imgpath='/data_1/weizhang/data/错图积累/1010/0侯凯_异常输出'
    src_path='/data_1/weizhang/data/错图积累/1010/new/result/result'
    out_path='/data_1/weizhang/data/错图积累/1010/new/result/result_renamed2'
    #run_path='/data_2/work/weizhang/share/model/加密/cryptopp_test'
    list_all_files(src_path)
    list_all_files2(ori_imgpath)
    for file in filelist:
        file = file.strip('\n')
        filename=file.split('/')[-1]
        index=filename.find('_')
        outfilename=filename[index+1:]
        outfile=file.replace(src_path,out_path)
        final_outfile=outfile.replace(filename,outfilename)
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
        for orifile in orilist:
            orifile = orifile.strip('\n')
            orifilename=orifile.split('/')[-1]
            imgindex1=orifilename.split('_')[-2]
            key1=orifilename.replace(imgindex1,'all')
            imgindex2=outfilename.split('_')[-2]
            key2=outfilename.replace(imgindex2,'all')
            if(key1==key2):
                shutil.copy(orifile,final_outfile.replace(imgindex2,imgindex1))
            
