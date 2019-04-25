#coding=utf-8

def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position
        
fpl=open('/data_1/weizhang/data/baoding/0107/规则比对/traffic/1625listlist_plate_js','w')
with open('/data_1/weizhang/data/baoding/0107/规则比对/traffic/1625list') as f:
    lines=f.readlines()
for line in lines:
    words=line.split('_')
    #print words[8]
    #sbbbh=words[1].split('/')[7]
    #print sbbbh
    index1=find_last(line,'/')
    img_name=line[index1+1:-1]
    print img_name
    sbbh=img_name.split('_')[0]
    # if index!=-1:
    #     print line[index+7:index+13]
    fpl.write(line[:-1]+' '+words[2]+' '+sbbh+'\n')