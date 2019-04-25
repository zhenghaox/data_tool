#coding=utf-8
import shutil
import os
if __name__ == '__main__':
    src_path='/data_1/weizhang/newpro/1107/WeiZhang/debug/Camera_config_files/320500'
    out_path='/data_1/weizhang/newpro/1107/WeiZhang/debug/Camera_config_files/320500(coded)'
    list=os.listdir(src_path)
    #for line1 in list:
       # print line1
    
    #f1=open('/data_1/weizhang/configfile/苏州/tmp/list')
    f2=open('/data_1/weizhang/configfile/suzhou.txt')
    #fimg=open('/media/e/weizhang/data/QHD/0808/jiaojingori/img.txt','w')
    #fcp=open('/media/e/weizhang/data/QHD/0808/jiaojingori/plate.txt','w')
    #lines1=f1.readlines()
    lines2=f2.readlines()
    for line11 in list:
        ewe=os.path.join(src_path,line11)
        line111=os.listdir(ewe)
        for line1 in line111:
            src_img_path=os.path.join(ewe,line1)
            index=names=line1.find('.')
            names=line1[:index]
            #print names
            for line2 in lines2:
                name2=line2.split(' ')[0]
                name=line2.split(' ')[-1]
                name = name[: -1]
                #print name          
                if names == name2:
                    out_img=os.path.join(out_path,name)
                    if not os.path.exists(out_img):
                        os.mkdir(out_img)
                    out_img_name=name+'.json'
                    out_img_path=os.path.join(out_img,out_img_name)
                    shutil.copy(src_img_path,out_img_path)
                    #print out_img_name
                    #names2=name[5].split('/')[-1][:-5]
                    #if os.path.exists('/data_1/weizhang/configfile/苏州/tmp/'+names+'.json'):
                   # shutil.copy('/data_1/weizhang/configfile/苏州/tmp/'+names+'.json','/data_1/weizhang/configfile/苏州/tmp/trainformed/'+name+'.json')
                    #fimg.write('/media/e/weizhang/data/QHD/0808/jiaojingori/img/'+names2+'.jpg'+'\n')
                    #fcp.write(name[1]+'\n')