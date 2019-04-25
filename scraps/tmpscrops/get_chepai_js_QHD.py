#coding=utf-8
import os
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position
list=[]
def list_all_files(now_dir):
    if os.path.isfile(now_dir):
        list.append(now_dir)
    else:
        listdir = os.listdir(now_dir)
        for i in listdir:
            if not os.path.isfile(i):
                i = now_dir + '/' + i
                list_all_files(i)     
src_path='/data_1/weizhang/data/SZ/0417'
fpl=open('/data_1/weizhang/data/SZ/0417_img_plate_js','w')
list_all_files(src_path)

for line in list:
    words=line.split('_')
    index1=find_last(line,'/')
    img_name=line[index1+1:]
    print img_name
    chepai=img_name.split('_')[1]
    sbbh=img_name.split('_')[0]
    fpl.write(line+' '+chepai+' '+sbbh+'\n')