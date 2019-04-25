#coding=utf-8
fpl=open('/data_1/weizhang/data/QHD/1201/1625_plate_js.txt','w')
with open('/data_1/weizhang/data/QHD/1201/1625_plate_num.txt') as f:
    lines=f.readlines()
for line in lines:
    words=line.split('/')
    sbbbh=words[7]
    print sbbbh
    fpl.write(line[:-1]+' '+sbbbh+'\n')