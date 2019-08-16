#coding=utf-8
import sys
sys.path.insert(0, '/data_2/car_reid/face_multiloss/python/')
reload(sys)
sys.setdefaultencoding('utf8')
import cv2
import caffe
import math
import numpy as np

if __name__ == "__main__":
    caffe.set_device(0)
    caffe.set_mode_gpu()
    deploy='/data_2/car_reid/model/car_reid.prototxt'    #deploy文件
    caffe_model='/data_2/car_reid/model/reid__iter_0.1.2.caffemodel'   #训练好的 caffemodel
    net = caffe.Net(deploy,caffe_model,caffe.TEST)
    img_path = '/data_2/car_reid/src/demoimg/0_220181001060836_冀C31700_0_0_49439151_5.jpg'
    img_name = img_path.split("/")[-1]
    img_in = cv2.imread(img_path)
    img_in = img_in[0:200]
    img_in=cv2.resize(img_in,(200,200))
    img_f = img_in.astype(np.float32)
    img_f = (img_f - 127.5) * 0.0078125
    img_f = np.transpose(img_f, (2, 0, 1))
    net.blobs['data'].data[...] = img_f    
    net.forward()
    prob1= net.blobs['inception_5b/pool_proj'].data[0].flatten()
    print prob1