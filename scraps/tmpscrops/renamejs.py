#coding=utf-8
import shutil
import os
if __name__ == '__main__':
    src_path='/data_1/tmp/json'
    out_path='/data_1/tmp/130300'
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    #f1=open('/data_1/weizhang/data/QHD/1127/conf/list')
    list=os.listdir(src_path)
    for l in list:
        src_json=os.path.join(src_path,l)
        jsname=l.split('_')[0]
        out_dir=os.path.join(out_path,jsname)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        out_json_name=jsname+'.json'
        out_json=os.path.join(out_dir,out_json_name)
        shutil.copy(src_json,out_json)
    # lines1=f1.readlines()
    # for line1 in lines1:
    #     index=names=line1.split('/')[-1].find('.')
    #     names=line1.split('/')[-1][:index]
    #     if os.path.exists('/data_1/weizhang/data/QHD/1127/conf/json/'+names+'.jpg.json'):
    #         shutil.copy('/data_1/weizhang/data/QHD/1127/conf/json/'+names+'.jpg.json','/data_1/weizhang/data/QHD/1127/conf/320300_old/'+names+'.json')               