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
    deploy='car_reid.prototxt'    #deploy文件
    caffe_model='../model/reid__iter_0.1.2.caffemodel'   #训练好的 caffemodel
    net = caffe.Net(deploy,caffe_model,caffe.TEST)
    img_path = '/data_2/car_reid/src/demoimg/0_220181001060836_冀C31700_0_0_49439151_5.jpg'
    img_name = img_path.split("/")[-1]
    #print img_name
    #img_name = img_path.split('/')[-1]
    img_in = cv2.imread(img_path)
    img_in = cv2.resize(img_in, (200, 400))
    img_1 = img_in[0:200]
    img_2 = img_in[200:400]

    img_f_1 = img_1.astype(np.float32)
    img_f_2 = img_2.astype(np.float32)

    img_f_1 = (img_f_1 - 127.5) * 0.0078125
    img_f_2 = (img_f_2 - 127.5) * 0.0078125

    img_f_1 = np.transpose(img_f_1, (2, 0, 1))
    img_f_2 = np.transpose(img_f_2, (2, 0, 1))


    net.blobs['data'].data[...] = img_f_1     
    net.forward()
    prob1= net.blobs['fc/7x7_s1'].data[0].flatten()

    net.blobs['data'].data[...] = img_f_2
    net.forward()
    prob2= net.blobs['fc/7x7_s1'].data[0].flatten()

    sum1 = 0
    sum2 = 0
    mul = 0
    for i in range(256):
        sum1 = sum1 + prob1[i] * prob1[i]
        sum2 = sum2 + prob2[i] * prob2[i]
        mul = mul + prob1[i] * prob2[i]
    sum1 = math.sqrt(sum1)
    sum2 = math.sqrt(sum2)
    cos = mul / (sum1 * sum2)
    cv2.putText(img_in, str(cos)[0:4], (0, 200), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255), 3)
    cv2.imshow('test', img_in)
    cv2.waitKey(0)