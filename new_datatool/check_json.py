#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
颜色是尽量按照up上面的颜色选取，部分内容统一使用蓝色
"""
import argparse
import cv2
import matplotlib.pyplot as plt
import json
# parser = argparse.ArgumentParser()
# parser.add_argument('--json_path', type=str, default ='config.json')
# parser.add_argument('--img_path', type=str, default='img.jpg')
# args = parser.parse_args()

def check_config(json_path,img_path,w_d,h_d):
     with open(json_path,'r') as load_f:
      load_dict = json.load(load_f)
      objects_label_list=load_dict['objects']
    # "width": 1200,
    # "height": 1600,
    # "w_d": 1,
    # "h_d": 1,
      img=cv2.imread(img_path)
      widthj=  load_dict['width']
      heightj=  load_dict['height']
      w_dj=  load_dict['w_d']
      h_dj=  load_dict['h_d']
      widthj=widthj/w_dj
      heightj=heightj/h_dj
      width=img.shape[1]/w_d
      height=img.shape[0]/h_d
      dw=float(float(widthj)/width)
      dh=float(float(heightj)/height)
      for item in objects_label_list:
          polygin=item['polygon']
          label=item['label']
          if label=='zebra-crossing':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i][0]/dw),int(polygin[i+1][1]/dh)),(255,0,255),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(255,0,255),4)
              continue
          if label=='stop-line':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(0,255,255),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(0,255,255),4)
              continue
          if label=='solid-line':#green
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(0,255,0),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(0,255,0),4)
              continue
          if label=='reid_mask':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(0,0,0),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(0,0,0),4)
              continue
          if label=='trafficlight_mask':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (150,100,255), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(150,100,255),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(150,100,255),4)
              continue
          if label=='straight-guideline':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,0), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(100,255,0),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(100,255,0),4)
              continue
          if label=='left-guideline':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(0,0,255),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(0,0,255),4)
              continue
          if label=='right-guideline':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,200,200), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(255,200,200),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(255,200,200),4)
              continue
          if label=='straight-left-guideline':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(0,0,255),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(0,0,255),4)
              continue
          if label=='straight-right-guideline':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,200,200), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(255,200,200),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(255,200,200),4)
              continue
          if label=='ConfYouZhuanRegion':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,150,100), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(100,130,100),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(100,130,100),4)
              continue
          
          if label=='straight-trafficlight':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (100,255,0), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(100,255,0),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(100,255,0),4)
              continue
          if label=='left-trafficlight':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(0,0,255),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(0,0,255),4)
              continue
          if label=='right-trafficlight':
              cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,200,200), 3)
              for i in range(len(polygin)-1):
                  cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(255,200,200),4)
              cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(255,200,200),4)
              continue
          else:#其余颜色用蓝色
              if objects_label_list.index(item)!=len(objects_label_list)-1:
                  cv2.putText(img, item['label'], (int(int(polygin[0][0]/dw)), int(int(polygin[0][1]/dw))), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 3)
                  for i in range(len(polygin)-1):
                      cv2.line(img, (int(polygin[i][0]/dw),int(polygin[i][1]/dh)), (int(polygin[i+1][0]/dw),int(polygin[i+1][1]/dh)),(255,0,0),4)
                  cv2.line(img, (int(polygin[-1][0]/dw),int(polygin[-1][1]/dh)), (int(polygin[0][0]/dw),int(polygin[0][1]/dw)),(255,0,0),4)
                  continue
              else:
                   break
          
      cv2.namedWindow('input_image', cv2.WINDOW_NORMAL) 
      cv2.resizeWindow('input_image',1000, 1000)
      cv2.imshow('input_image',img)
      cv2.waitKey(0)
      cv2.destroyAllWindows()

if __name__== '__main__':
    # json_path=args.json_path
    # img_path=args.img_path
    w_d=2
    h_d=2
    json_path='/data_1/weizhang/VIR_models/models/Camera_config_files/321300/4262/4262_2.json'
    img_path='/data_1/weizhang/data/错图积累/1226/img/4262+苏N33P98+1208+4262+02+0+@2862000@@@2019-12-23#07#21#00+a0+2.jpg'
    check_config(json_path,img_path,w_d,h_d)
