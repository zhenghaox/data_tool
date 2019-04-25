#coding=utf-8
testFile = open('/media/d/work/weizhang/1', 'w')
trainFile = open('/media/d/work/weizhang/2', 'w')
num=0
with open('/media/d/work/weizhang/test.txt') as f:
    lines=f.readlines()
for line in lines:
    num=num+1
    if num%5 ==1:
        testFile.write(line)
    else:
        trainFile.write(line)
testFile.close()
trainFile.close()
