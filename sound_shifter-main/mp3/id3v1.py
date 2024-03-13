# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 23:21:00 2024

@author: 14000
"""

#coding: UTF-8
import os
import string
import base64
import chardet
'''
解析mp3，获取TAG_V1
'''

def parse(fileObj,version='v1'):
    fileObj.seek(0,2)
    if(fileObj.tell()<128):
        return False
    fileObj.seek(-128,2)
    tag_data=fileObj.read()
    if(tag_data[0:3] != b'TAG'):
	    return False
    return getTag(tag_data)

def decodeData(bin_seq):
    result=chardet.detect(bin_seq)
    # print(result)
    if(result['confidence']>0):
        try:
            return bin_seq.decode(result['encoding'])
        except:
            return 'Decode fail'

def getTag(tag_data):
    STRIP_CHARS=b'\x00'
	
    tags={}
    tags['title']=tag_data[3:33].strip(STRIP_CHARS)
    if(tags['title']):
	    tags['title'] = decodeData(tags['title'])
    tags['artist']=tag_data[33:63].strip(STRIP_CHARS)
    if(tags['artist']):
        tags['artist']=decodeData(tags['artist'])
    tags['genre'] = ord(tag_data[127:128])
    return tags

f=open('../test_audio_files/See You Again.128.mp3', 'rb')
t=parse(f)
print(t)
