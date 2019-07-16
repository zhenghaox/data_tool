#!/usr/bin/env python
#coding=utf-8
import os
import sys
import cv2
from itertools import islice
from xml.dom.minidom import Document

labels='/data_1/weizhang/data/铭牌文件检测/text'
imgpath='/data_1/weizhang/data/铭牌文件检测/mark/'
xmlpath_new='/data_1/weizhang/data/铭牌文件检测/xml/'
if not os.path.exists(xmlpath_new):
    os.mkdir(xmlpath_new)
foldername='train_images'


def insertObject(doc, datas):
    obj = doc.createElement('object')
    name = doc.createElement('name')
    name.appendChild(doc.createTextNode(datas[0]))
    obj.appendChild(name)
    pose = doc.createElement('pose')
    pose.appendChild(doc.createTextNode('Unspecified'))
    obj.appendChild(pose)
    truncated = doc.createElement('truncated')
    truncated.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(truncated)
    difficult = doc.createElement('difficult')
    difficult.appendChild(doc.createTextNode(str(0)))
    obj.appendChild(difficult)
    bndbox = doc.createElement('bndbox')
    
    x1 = doc.createElement('x1')
    x1.appendChild(doc.createTextNode(str(int(datas[1]))))
    bndbox.appendChild(x1)  
    y1 = doc.createElement('y1')                
    y1.appendChild(doc.createTextNode(str(int(datas[2]))))
    bndbox.appendChild(y1)                
    x2 = doc.createElement('x2')                
    x2.appendChild(doc.createTextNode(str(int(datas[3]))))
    bndbox.appendChild(x2)  
    y2 = doc.createElement('y2')
    y2.appendChild(doc.createTextNode(str(int(datas[4]))))
    bndbox.appendChild(y2)  
    x3 = doc.createElement('x3')                
    x3.appendChild(doc.createTextNode(str(int(datas[5]))))
    bndbox.appendChild(x3)                
    y3 = doc.createElement('y3')                
    y3.appendChild(doc.createTextNode(str(int(datas[6]))))
    bndbox.appendChild(y3)
    x4 = doc.createElement('x4')
    x4.appendChild(doc.createTextNode(str(int(datas[7]))))
    bndbox.appendChild(x4)  
    y4 = doc.createElement('y4')                
    y4.appendChild(doc.createTextNode(str(int(datas[8]))))
    bndbox.appendChild(y4)   
    xmin = doc.createElement('xmin')
    xmin.appendChild(doc.createTextNode(str(int(datas[9]))))
    bndbox.appendChild(xmin)   
    ymin = doc.createElement('ymin')                
    ymin.appendChild(doc.createTextNode(str(int(datas[10]))))
    bndbox.appendChild(ymin)
    xmax = doc.createElement('xmax')                
    xmax.appendChild(doc.createTextNode(str(int(datas[11]))))
    bndbox.appendChild(xmax)              
    ymax = doc.createElement('ymax')    
    if  '\r' == str(int(datas[12]))[-1] or '\n' == str(int(datas[12]))[-1]:
        data = str(int(datas[12]))[0:-1]
    else:
        data = str(int(datas[12]))
    ymax.appendChild(doc.createTextNode(data))
    bndbox.appendChild(ymax)
    obj.appendChild(bndbox)                
    return obj

def create():
    for walk in os.walk(labels):
        for each in walk[2]:
            fidin=open(walk[0] + '/'+ each,'r')
            pictureName = each.replace('.txt', '.jpg')
            imageFile = imgpath + pictureName
            #print pictureName
            img = cv2.imread(imageFile)
            imgSize = img.shape
            objIndex = 0
            for data in islice(fidin, 1, None):        
                objIndex += 1
                data=data.strip('\n')
                datas = data.split(' ')
                if 13 != len(datas):
                    print 'bounding box information error'
                    continue 
                if 1 == objIndex:
                    xmlName = each.replace('.txt', '.xml')
                    f = open(xmlpath_new + xmlName, "w")
                    doc = Document()
                    annotation = doc.createElement('annotation')
                    doc.appendChild(annotation)
                    
                    folder = doc.createElement('folder')
                    folder.appendChild(doc.createTextNode(foldername))
                    annotation.appendChild(folder)
                    
                    filename = doc.createElement('filename')
                    filename.appendChild(doc.createTextNode(pictureName))
                    annotation.appendChild(filename)
 
                    size = doc.createElement('size')
                    width = doc.createElement('width')
                    width.appendChild(doc.createTextNode(str(imgSize[1])))
                    size.appendChild(width)
                    height = doc.createElement('height')
                    height.appendChild(doc.createTextNode(str(imgSize[0])))
                    size.appendChild(height)
                    depth = doc.createElement('depth')
                    depth.appendChild(doc.createTextNode(str(imgSize[2])))
                    size.appendChild(depth)
                    annotation.appendChild(size)
                               
                    annotation.appendChild(insertObject(doc, datas))
                else:
                    annotation.appendChild(insertObject(doc, datas))
            try:
                f.write(doc.toprettyxml(indent = '    '))
                f.close()
                fidin.close()
            except:
                pass
   
          
if __name__ == '__main__':
    create()