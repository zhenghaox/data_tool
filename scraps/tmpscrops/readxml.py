import os

import cv2

import xml.etree.ElementTree as et

src_img_path="/media/huangkaijun/3f178b95-bfda-4414-a292-10e1f7fdee9e/car_data/许昌数据/违反导向/ori"

src_xml_path="/media/huangkaijun/3f178b95-bfda-4414-a292-10e1f7fdee9e/car_data/许昌数据/违反导向/xml"



file_path = open("/media/huangkaijun/3f178b95-bfda-4414-a292-10e1f7fdee9e/car_data/许昌数据/违反导向/ori.list",'r')

dst_path = open("/media/huangkaijun/3f178b95-bfda-4414-a292-10e1f7fdee9e/car_data/许昌数据/违反导向/img_all.list",'w')

DICT={}

count=0

for line in file_path.readlines():

    key=line.split("/")[-1].split(".jpg")[0]

    DICT[key]=line.split("\n")[0]



for root2, dirs2, files2 in os.walk(src_xml_path):

    for filename2 in files2:

        tree=et.parse(os.path.join(src_xml_path, filename2))

        xml_root=tree.getroot()



        newKey = filename2.split(".xml")[0]

        dst_path.write(DICT[newKey]+"$")

        index=0

        for obj in xml_root.findall('object'):

            car_reid=obj.find('name').text

            if car_reid=='ReID_1':

                bndbox=obj.find('bndbox')

                xmin = str(bndbox.find('xmin').text)

                ymin = str(bndbox.find('ymin').text)

                xmax = str(bndbox.find('xmax').text)

                ymax = str(bndbox.find('ymax').text)

                if index!=0:

                    dst_path.write(","+xmin+","+ymin+","+xmax+","+ymax)

                else:

                    dst_path.write(xmin + "," + ymin + "," + xmax + "," + ymax)

                index+=1

        dst_path.write("\n")