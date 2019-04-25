#! /usr/bin/env python
# -*- coding:utf-8 -*-
# xml 转 json
# xml2json.py
# Version 1.0

from xml.parsers.expat import ParserCreate
import json
import os

class Xml2Json:
    LIST_TAGS = ['COMMANDS']
    
    def __init__(self, data = None):
        self._parser = ParserCreate()
        self._parser.StartElementHandler = self.start
        self._parser.EndElementHandler = self.end
        self._parser.CharacterDataHandler = self.data
        self.result = None
        if data:
            self.feed(data)
            self.close()
        
    def feed(self, data):
        self._stack = []
        self._data = ''
        self._parser.Parse(data, 0)

    def close(self):
        self._parser.Parse("", 1)
        del self._parser

    def start(self, tag, attrs):
        assert attrs == {}
        assert self._data.strip() == ''
        self._stack.append([tag])
        self._data = ''

    def end(self, tag):
        last_tag = self._stack.pop()
        assert last_tag[0] == tag
        if len(last_tag) == 1: #leaf
            data = self._data
        else:
            if tag not in Xml2Json.LIST_TAGS:
                # build a dict, repeating pairs get pushed into lists
                data = {}
                for k, v in last_tag[1:]:
                    if k not in data:
                        data[k] = v
                    else:
                        el = data[k]
                        if type(el) is not list:
                            data[k] = [el, v]
                        else:
                            el.append(v)
            else: #force into a list
                data = [{k:v} for k, v in last_tag[1:]]
        if self._stack:
            self._stack[-1].append((tag, data))
        else:
            self.result = {tag:data}
        self._data = ''

    def data(self, data):
        self._data = data

if __name__ == '__main__':
    src_path='/data_1/weizhang/data/baoding/0107/规则比对/traffic/test/1205xml'
    out_path='/data_1/weizhang/data/baoding/0107/规则比对/traffic/test/txt_new'
    lists=os.listdir(src_path)
    for list in lists:
        result=[]
        print list
        listname=list[:-4]
        xml = open(src_path+'/'+list, 'r').read()
        result = Xml2Json(xml).result
        annotation=result['annotation']
        segmented=annotation['segmented']
        objects=annotation['object']
        #objects.ex
        print 'name' in objects
        num = 0
        datalist=[]
        if 'name' in objects:    
            name=objects['name']
            rect=objects['bndbox']
            xmin=rect['xmin']
            ymin=rect['ymin']
            xmax=rect['xmax']
            ymax=rect['ymax']
            if name == 'hei' or name =='hei-heng' or name == 'hei-shu':
                continue
            num=num+1
            newlist=[name,xmin,ymin,xmax,ymax]
            datalist.append(newlist)
            if len(datalist)>0:
                savetxt=open(out_path+'/'+listname+'.txt','w')
                savetxt.write(str(num)+'\n')
                for t in range(0,len(datalist)):
                    savetxt.write(datalist[t-1][0]+' '+datalist[t-1][1]+' '+datalist[t-1][2]+' '+datalist[t-1][3]+' '+datalist[t-1][4]+'\n')
        else:
            for object in objects:
                name=object['name']
                rect=object['bndbox']
                xmin=rect['xmin']
                ymin=rect['ymin']
                xmax=rect['xmax']
                ymax=rect['ymax']
                if name == 'hei' or name =='hei-heng' or name == 'hei-shu':
                    continue
                num=num+1
                newlist=[name,xmin,ymin,xmax,ymax]
                datalist.append(newlist)
            if len(datalist)>0:
                savetxt=open(out_path+'/'+listname+'.txt','w')
                savetxt.write(str(num)+'\n')
                for t in range(0,len(datalist)):
                    savetxt.write(datalist[t-1][0]+' '+datalist[t-1][1]+' '+datalist[t-1][2]+' '+datalist[t-1][3]+' '+datalist[t-1][4]+'\n')

