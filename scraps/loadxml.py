import re
import math
import random
import sys
import xml.dom.minidom

dom = xml.dom.minidom.parse('/media/d/work/weizhang/trafficlight/cropedAnn/3.xml')
root = dom.documentElement
res = root.getElementsByTagName('object')
#res1 = root.getElementsByTagName('object')[0].firstChild.data
xy = np.zeros((len(res), 5), np.float32)
#print res1
t=1
for id, r in enumerate(res):
    x1 = float(r.getElementsByTagName('xmin')[0].firstChild.data)
    y1 = float(r.getElementsByTagName('ymin')[0].firstChild.data)
    x2 = float(r.getElementsByTagName('xmax')[0].firstChild.data)
    y2 = float(r.getElementsByTagName('ymax')[0].firstChild.data)
            
