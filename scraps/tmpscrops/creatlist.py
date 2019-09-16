#coding=utf-8
import os
   
src_path='/data_1/weizhang/data/all/后加/0821/txt'
savetxt=open('/data_1/weizhang/data/all/后加/0821/list.txt','w')
list=os.listdir(src_path)
for line in list:
    name=line[:-4]
    savetxt.write('cut/'+name+'.jpg'+' '+'txt/'+name+'.txt'+'\n')