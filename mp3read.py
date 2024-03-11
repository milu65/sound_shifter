# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 01:19:52 2024

@author: 14000
"""
import struct

encodings = ['GBK', 'UTF-16', 'UTF-16BE', 'UTF-8']

def read_mp3_bytes(file_path):
    try:
        with open(file_path, 'rb') as mp3_file:
            # 读取整个文件的字节数据
            mp3_bytes = mp3_file.read()
            return mp3_bytes
    except Exception as e:
        print(f"Error: {e}")
        return None

def id3v2header_read(data):
    id3v2={}
    id3v2["header"]=data[:3].decode('utf-8')
    id3v2["version"]=data[3]
    id3v2["revision"]=data[4]
    id3v2["flag"]=data[5]
    id3v2["size"]=(data[6] << 21 | data[7] << 14 |
                       data[8] << 7 | data[9])
    return id3v2


if __name__ == "__main__":
    mp3_file_path = "D:/code/python/mp3/See You Again.128.mp3"
    mp3_data = read_mp3_bytes(mp3_file_path)

    if mp3_data:
        print(f"Successfully read {mp3_file_path} as bytes.")
        # 在这里，你可以对 mp3_data 进行进一步的处理
    else:
        print("Failed to read the MP3 file.")
        
    id3v2_result=id3v2header_read(mp3_data)
    print("ID3v1 Tag Information:")
    print("Header:", id3v2_result["header"])
    print("Version:", id3v2_result["version"],".",id3v2_result["revision"])
    print("Flag:", id3v2_result["flag"])
    print("Size:", id3v2_result["size"])
    
    
    