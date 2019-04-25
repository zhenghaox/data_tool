#coding=utf-8

fimg=open('/media/e/weizhang/test/0608/pass/notsure_img.txt','w')
fpl=open('/media/e/weizhang/test/0608/pass/notsure_cp.txt','w')
with open('/media/e/weizhang/test/0608/pass/notsure.txt') as f:
    lines=f.readlines()
for line in lines:
    if line[-6:-5]=='5' or  line[-6:-5]=='4' or  line[-6:-5]=='3' or  line[-6:-5]=='2':
        continue
    index=line.find('_╝╜')
    if index!=-1:
        fimg.write(line)
        print line[index+7:index+13]
        fpl.write('冀'+line[index+7:index+13]+'\n')
    