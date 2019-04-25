import cv2

with open('/media/d/work/weizhang/trafficlight/123') as f:
    lines=f.readlines()
for line in lines:
    img1=cv2.imread('/media/d/work/weizhang/trafficlight/JPEGImages/'+line[:-1])
    imgsz = [img1.shape[1], img1.shape[0]]
    print imgsz
    img=img1[:imgsz[1]/2,imgsz[0]/7:,:]
    cv2.imwrite('/media/d/work/weizhang/trafficlight/cropedimg/'+line[:-1],img)