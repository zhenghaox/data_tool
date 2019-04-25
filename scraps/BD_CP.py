#coding=utf-8

fpl=open('/media/e/weizhang/data/baoding/6.11/use/cp','w')
with open('/media/e/weizhang/data/baoding/6.11/use/img') as f:
    lines=f.readlines()
for line in lines:
    words=line.split('@')
    print words[3]
    # index=line.find('_╝╜')
    # if index!=-1:
    #     print line[index+7:index+13]
    fpl.write(words[3]+'\n')