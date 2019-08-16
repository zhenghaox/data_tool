#coding=utf-8
import os
   
src_path='/data_1/weizhang/data/all/ori/neg/fixedtxt'
savetxt=open('/data_1/weizhang/data/all/ori/neg/neg.txt','w')
list=os.listdir(src_path)
for line in list:
    name=line[:-4]
    savetxt.write('img/'+name+'.jpg'+' '+'fixedtxt/'+name+'.txt'+'\n')