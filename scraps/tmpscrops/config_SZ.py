#coding=utf-8
import os
import shutil
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position
srcpath='/data_1/weizhang/configfile/苏州/bak/img/json'  
outpath='/data_1/weizhang/configfile/苏州/bak/img/js' 
list=os.listdir(srcpath) 
for line in list:
    sbbh=line.split('_')[0]
    outname=sbbh+'.json'
    srcjs=os.path.join(srcpath,line)
    outjs=os.path.join(outpath,outname)
    shutil.copy(srcjs,outjs)
    print sbbh  
# fpl=open('/data_1/weizhang/data/错图积累/苏州/1211/img_plate_js','w')
# with open('/data_1/weizhang/data/错图积累/苏州/1211/list') as f:
#     lines=f.readlines()
# for line in lines:
#     words=line.split('_')
#     #sbbbh=words[1].split('/')[7]
#     #print sbbbh
#     index1=find_last(line,'/')
#     img_name=line[index1+1:-1]
#     sbbh=img_name.split('_')[0]
#     # if index!=-1:
#     #     print line[index+7:index+13]
#     fpl.write(line[:-1]+' '+words[8]+' '+sbbh+'\n')