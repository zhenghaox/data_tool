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
src_path='/data_1/weizhang/data/错图积累/1127绍兴张家口/张家口/0侯凯_异常输出'
fpl=open('/data_1/weizhang/data/错图积累/1127绍兴张家口/张家口/0侯凯_异常输出.txt','w')
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

    #imgindex=''
    key=img_name.replace(imgindex,'all')
    dic.setdefault(key,[]).append(line)
for key1, values in dic.items():
    index1=find_last(values[0],'/')
    img_name=values[0][index1+1:]

    chepai=img_name.split('_')[1]
    #chepai=img_name.split('_')[7]
    sbbh=img_name.split('_')[0]
    #sbbh='000001'
    label=img_name.split('_')[-1][:-4]  
    imgindex=img_name.split('_')[-2]

    if  len(values)==1:
        fpl.write(str(values[0])+' '+chepai+' '+sbbh+' '+label+'\n')
    elif len(values)==2:
        fpl.write(str(values[0]).replace(imgindex,'a1')+' '+str(values[1]).replace(values[1].split('_')[-2],'a2')+' '+chepai+' '+sbbh+' '+label+'\n')
    elif len(values)==3:
        fpl.write(str(values[0]).replace(imgindex,'a1')+' '+str(values[1]).replace(values[1].split('_')[-2],'a2')+' '+str(values[2]).replace(values[2].split('_')[-2],'a3')+' '+chepai+' '+sbbh+' '+label+'\n')
    #fpl.write(line+' '+chepai+' '+sbbh+'\n')
    #fpl.write(line+' '+chepai+' '+label+'\n')
    