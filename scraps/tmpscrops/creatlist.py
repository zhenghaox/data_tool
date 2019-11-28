#coding=utf-8
import os
   
src_path='/data_1/weizhang/data/all/后加/违法_红绿灯_20190902-OK-已检查/新建文件夹/result/all/txt'
savetxt=open('/data_1/weizhang/data/all/后加/违法_红绿灯_20190902-OK-已检查/新建文件夹/result/all/txt.txt','w')
list=os.listdir(src_path)
for line in list:
    name=line[:-4]
    savetxt.write('../后加/违法_红绿灯_20190902-OK-已检查/新建文件夹/result/all/cut/'+name+'.jpg'+' '+'../后加/违法_红绿灯_20190902-OK-已检查/新建文件夹/result/all/txt/'+name+'.txt'+'\n')