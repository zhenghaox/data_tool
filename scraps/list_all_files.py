#coding=utf-8
import sys
import os  
f=open('/data_1/weizhang/data/安全带打电话/南昌/0404.list','w')
def list_all_files(now_dir):  
    if os.path.isfile(now_dir):  
        print now_dir
        if str(now_dir)[-4:]=='.jpg':
            f.write(str(now_dir)+'\n')  
    else:  
        listdir = os.listdir(now_dir)  
        for i in listdir:  
            if os.path.isfile(i):   
                print i                 
            else:  
                i = now_dir + '/' + i  
                list_all_files(i)  
#f.close()  
#list_all_files(sys.argv[1])  /media/e/weizhang/data/baoding/0611
list_all_files('/data_1/weizhang/data/安全带打电话/南昌/0404')