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
src_path='/data_1/weizhang/data/错图积累/1010/0侯凯_异常输出'
fpl=open('/data_1/weizhang/data/错图积累/1010/0侯凯_异常输出.txt','w')
list_all_files(src_path)
dic = {}
for line in list:
    if line[-4:]!='.jpg':
        continue
    words=line.split('_')
    index1=find_last(line,'/')
    img_name=line[index1+1:]
    # print img_name
    # chepai=img_name.split('_')[1]
    # #chepai=img_name.split('_')[10]
    # sbbh=img_name.split('_')[0]
    # label=img_name.split('_')[-1][:-4]
    imgindex=img_name.split('_')[-2]
    key=img_name.replace(imgindex,'all')
    dic.setdefault(key,[]).append([img_name,line])
for key, values in dic.items():
    print img_name,line
    chepai=img_name.split('_')[1]
    #chepai=img_name.split('_')[10]
    sbbh=img_name.split('_')[0]
    label=img_name.split('_')[-1][:-4]  
    imgindex=img_name.split('_')[-2]
    if len(values)==1:
        fpl.write(line+' '+chepai+' '+sbbh+' '+label+'\n')
    else
        
    #fpl.write(line+' '+chepai+' '+sbbh+'\n')
    #fpl.write(line+' '+chepai+' '+label+'\n')
    