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
src_path='/data_1/weizhang/data/错图积累/1010/张家港现场/test'
fpl=open('/data_1/weizhang/data/错图积累/1010/张家港现场/test.txt','w')
list_all_files(src_path)

for line in list:
    if line[-4:]!='.jpg':
        continue
    words=line.split('_')
    index1=find_last(line,'/')
    img_name=line[index1+1:]
    print img_name
    #chepai=img_name.split('_')[1]
    chepai=img_name.split('_')[10]
    sbbh=img_name.split('_')[0]
    label=img_name.split('_')[-1][:-4]
    #fpl.write(line+' '+chepai+' '+sbbh+'\n')
    #fpl.write(line+' '+chepai+' '+label+'\n')
    fpl.write(line+' '+chepai+' '+sbbh+' '+label+'\n')