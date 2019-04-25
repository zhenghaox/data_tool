import yaml
import os
import cv2

def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position

f=open('/media/d/work/SSD/caffe/data/dataset_train_rgb/train.yaml')
x=yaml.load(f)
for x1 in x:
    if len(x1['boxes']):
       img=cv2.imread('/media/d/work/SSD/caffe/data/dataset_train_rgb/'+x1['path'][2:])
     #   print x1['boxes']
       name = x1['path'][find_last(x1['path'], '/') + 1:-4]
       cv2.imwrite('/media/d/work/SSD/caffe/data/dataset_train_rgb/JPEGImages/'+name+'.jpg',img)
       f=open('/media/d/work/SSD/caffe/data/dataset_train_rgb/label/'+name+'.txt','w')
       x2=x1['boxes']
       f.write(str(len(x2))+'\n')
       for num in range(0,len(x2)):
           #print x2[num]
           f.write(x2[num]['label']+' '+str(x2[num]['x_min'])+' '+str(x2[num]['y_min'])+' '+str(x2[num]['x_max'])+' '+str(x2[num]['y_max'])+'\n')