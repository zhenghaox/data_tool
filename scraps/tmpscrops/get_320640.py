#coding=utf-8
fpl=open('/data_1/weizhang/data/0626/all/320640/train_SZ.txt','w')
with open('/data_1/weizhang/data/0626/all/train.txt') as f:
    lines=f.readlines()
for line in lines:
    words=line.split(' ')
    img=words[0]
    xml=words[1]

    img_320640=img.split('_')
    xml_320640=img.split('_')
    if img_320640[-3] == '320' or img_320640[-3] == '640':
        fpl.write(img+' '+xml[:-1]+'\n')
    #print words[8]
    # index=line.find('_╝╜')
    # if index!=-1:
    #     print line[index+7:index+13]
    