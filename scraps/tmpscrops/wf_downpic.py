# -*- coding: utf-8 -*-
# !/usr/bin/env python
#
# v0.1 20190110 基础功能 数据部
# 
# 说明：
# 读取csv中图片链接，按照指定名称下载， 下载到download目录下
# 
# 1.安装依赖库
# sudo apt install python3-pip
# pip3 install requests
#
# 2.修改你要下载csv文件名称
# csv_path="./xxx.csv"
#
# 3.使用
# python3 wf_downpic.py 

import requests
import csv,os
from contextlib import closing

#修改你的cs文件名
csv_path="/home/xuzhenghao/下载/201904170952_suzhou.csv"
download_path="/data_1/weizhang/data/SZ/0417/"

#http请求超时设置
timeout = 200

def CheckDir(dir):
    if not os.path.exists(dir):
      os.makedirs(dir)
    pass

CheckDir(download_path)

 
#下载
def DownloadFile(img_url, dir_name, img_name):
    # check_download_dir(folder_name)
    try:
        with closing(requests.get(img_url,  stream=True, timeout=timeout)) as r:
            rc = r.status_code
            if 299 < rc or rc < 200:
                print('returnCode%s\t%s' % (rc, img_url))
                return
            content_length = int(r.headers.get('content-length', '0'))

            if content_length == 0:
                print('size0\t%s' % img_url)
                return
            try:
                with open(os.path.join(dir_name, img_name), 'wb') as f:
                    for data in r.iter_content(1024):
                        f.write(data)
                print('download success: %s \t filename:%s \t size: %s' %( img_url,img_name,content_length))
            except:
                print('save fail \t%s' % img_url)
    except:
        print('requests fail \t%s' % img_url)

read_csv = csv.reader(open(csv_path))

for row in read_csv:
    img_url = row[0]
    file_name = row[1]
    if img_url != "picture_path":
        DownloadFile(img_url, download_path, file_name)

