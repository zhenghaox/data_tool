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
src_path='/data_1/weizhang/data/all/ori/neg/xml'
savetxt=open('/data_1/weizhang/data/all/ori/neg/neg.test','w')
list_all_files(src_path)

#savetxt=open('/data_1/weizhang/data/BDdone/up/0225list','w')
#with open('/data_1/weizhang/data/BDdone/up/xmllist') as f:
#    lines=f.readlines()
for line in list:
    index=find_last(line,'/')
    name=line[index+1:-4]
    savetxt.write('img/'+name+'.jpg'+' '+'xml/'+name+'.xml'+'\n')
