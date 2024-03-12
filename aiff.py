# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 15:38:41 2024

@author: 14000
"""

import struct

def read_aiff_file(file_path):
    with open(file_path, 'rb') as file:
        # AIFF Header
        form_chunk_id = file.read(4)
        if form_chunk_id != b'FORM':
            print("Not a valid AIFF file (missing FORM header).")
            return

        form_chunk_size = struct.unpack('>I', file.read(4))[0]
        form_type = file.read(4)
        print("AIFF Head")
        print(f"Form Type: {form_type.decode('ascii')}")
        print(f"Form Size: {form_chunk_size} bytes\n")

        # Chunk
        while True:
            chunk_id = file.read(4)
            if not chunk_id:
                break  # end
            
            # to make sure match
            #'''
            file_position = file.tell()  # 获取当前文件指针位置
            remaining_bytes = file.read(4)  # 尝试读取 4 个字节的数据
            
            if len(remaining_bytes) == 4:
                # 文件指针移动回原位置
                file.seek(file_position)
                chunk_size = struct.unpack('>I', remaining_bytes)[0]
                # 接下来的处理...
            else:
                print("Error: Unable to read 4 bytes from the file.")
                return
            #'''
            
            chunk_size = struct.unpack('>I', file.read(4))[0]
            
            print("chunk_size:",chunk_size,"\n")
            #print(chunk_id)
            
            # COMM
            if chunk_id == b'COMM':
                sample_channels = struct.unpack('>H', file.read(2))[0]
                num_sample_frames = struct.unpack('>I', file.read(4))[0]
                sample_size = struct.unpack('>H', file.read(2))[0]
                file.read(2) #useless1
                sample_rate = int.from_bytes(file.read(2), byteorder='big')
                file.read(6) #useless2
                
                print("COMM Chunk")
                print(f"Channels: {sample_channels}")
                print(f"Sample Frames: {num_sample_frames}")
                print(f"Sample Size: {sample_size} bits")
                print(f"Sample Rate: {sample_rate/1000} kHz\n")

            # SSND
            elif chunk_id == b'SSND':
                offset = struct.unpack('>I', file.read(4))[0]
                block_size = struct.unpack('>I', file.read(4))[0]
                
                print("SSNR Chunk")
                print(f"Data Offset: {offset} bytes")
                print(f"Block Size: {block_size} bytes\n")

                # data
                audio_data = file.read(chunk_size)
                return audio_data
                




def main():
    file_path = 'D:/code/python/aiff/sample-3.aif'  # path
    data=read_aiff_file(file_path)
    

if __name__ == "__main__":
    main()


