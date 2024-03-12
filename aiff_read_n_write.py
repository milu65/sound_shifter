# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 23:10:29 2024

@author: 14000
"""
import array
import struct


def pcm_to_adpcm(pcm_data):
    indexTable = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]
    stepsizeTable = [
        7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
        50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230,
        253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963,
        1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327,
        3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487,
        12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
    ]

    output_buffer = 0
    buffer_step = True
    adpcm_data = array.array('h')

    # ADPCM编码过程
    for i in range(0, len(pcm_data), 2):
        val = struct.unpack('>h', pcm_data[i:i+2])[0]
        diff = val
        sign = 0

        if diff < 0:
            sign = 8
            diff = -diff

        delta = 0
        vpdiff = stepsizeTable[output_buffer >> 3]

        if diff >= vpdiff:
            delta = 4
            diff -= vpdiff

        vpdiff >>= 1

        if diff >= vpdiff:
            delta |= 2
            diff -= vpdiff

        vpdiff >>= 1

        if diff >= vpdiff:
            delta |= 1

        if sign != 0:
            val = val - stepsizeTable[output_buffer >> 3]
        else:
            val = val + stepsizeTable[output_buffer >> 3]

        if val > 32767:
            val = 32767
        elif val < -32768:
            val = -32768

        delta |= sign
        index = output_buffer + indexTable[delta]

        if index < 0:
            index = 0
        elif index > 88:
            index = 88

        step = stepsizeTable[index]

        if buffer_step:
            output_buffer = delta & 0x0F
        else:
            adpcm_data.append(((delta << 4) & 0xF0) | output_buffer)
        buffer_step = not buffer_step

    return adpcm_data


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
 
               
def write_adpcm_to_aiff(original_aiff_path, adpcm_data, output_file):
    # 打开原始 AIFF 文件并读取其内容
    with open(original_aiff_path, 'rb') as original_file:
        original_data = original_file.read()

    # 找到原始 AIFF 文件中的 DATA 块位置
    #print("read success")
    data_chunk_start = original_data.find(b'SSND') + 4
    print("find success")
    data_chunk_size = struct.unpack('>I', original_data[data_chunk_start:data_chunk_start + 4])[0]

    # write back
    
    with open(output_file, 'wb') as output_stream:
        # header
        output_stream.write(original_data[:42])

        #chunk size
        output_stream.write(struct.pack('>I', len(adpcm_data)+8))
        print(adpcm_data)

        #offset
        output_stream.write(original_data[46:54])

        # data
        output_stream.write(adpcm_data.tobytes())

        # others
        if len(adpcm_data) < data_chunk_size:
            output_stream.write(original_data[data_chunk_start + 4 + len(adpcm_data):])





def main():
    file_path = 'aiff/sample-3.aif'  # path
    file_path2 = 'aiff/3ad.aif'  # path
    data=read_aiff_file(file_path)
    print("len(data):",len(data))
    adpcm_data=pcm_to_adpcm(data)
    print("len(adpcm_data):",len(adpcm_data))

    import soundfile
    import numpy as np
    import json

    data = np.frombuffer(data, dtype='>i2').reshape(-1, 2)
    soundfile.write("out.aif", data.astype(np.int16), 48000, "IMA_ADPCM", format="AIFF")
    write_adpcm_to_aiff(file_path, adpcm_data,file_path2)
    print("success")



if __name__ == "__main__":
    main()