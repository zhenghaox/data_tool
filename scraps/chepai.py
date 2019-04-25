#!/usr/bin/env python
# coding:utf-8

import os
import re
import sys
import json
import cv2
import numpy as np
from lxml import etree
import xml.etree.ElementTree as et
from lxml.etree import Element, SubElement, tostring
from PIL import Image, ImageDraw
import shutil

image_folder1 = '/media/wangsai/808513ea-317d-453f-b525-fa0ae5b95925/dataset/2018.04.12jiaotongchangjingfenge/6023不按规定车道/审核通过/20180416100100/20180409'
image_folder2 = '/media/wangsai/808513ea-317d-453f-b525-fa0ae5b95925/dataset/2018.04.12jiaotongchangjingfenge/6023不按规定车道/审核通过/20180416100100/20180409-select'

image_list = '/media/wangsai/808513ea-317d-453f-b525-fa0ae5b95925/dataset/2018.04.12jiaotongchangjingfenge/6023不按规定车道/审核通过/20180416100100/tmp.txt'

chepai_file = '/media/wangsai/808513ea-317d-453f-b525-fa0ae5b95925/dataset/2018.04.12jiaotongchangjingfenge/6023不按规定车道/审核通过/20180416100100/chepai.txt'

txt_file_fd = open(chepai_file, 'w')
txt_list_fd = open(image_list, 'w')

number = 0;

if __name__ == '__main__':
    for root, dirs, files in os.walk(image_folder1):
        for filename in files:
            image_path1 = os.path.join(image_folder1, filename)
            image_path2 = os.path.join(image_folder2, filename)

            split_name = re.split('_╝╜|_|\.', filename)

            print 'split_name : ',split_name
            if split_name[5] == '1':

                shutil.copyfile(image_path1, image_path2)

                txt_file_fd.write('冀' + split_name[1] + '\n')
                txt_list_fd.write(image_path1 + '\n')

                number += 1
                if number > 200:
                    break

    txt_file_fd.close()
    txt_list_fd.close()