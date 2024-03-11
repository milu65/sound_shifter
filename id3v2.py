
"""
处理mp3解析，获取ID3V2信息
"""
import struct

encodings = ['GBK', 'UTF-16', 'UTF-16BE', 'UTF-8']


def parse_ID3V2_frames(frames_bin):
    """
    解析帧数据
    :param frames_bin:
    :return:
    """
    pointer = 0
    frames_bin_size = len(frames_bin)
    frames = {}
    while pointer < frames_bin_size - 10:
        frame_header_bin = frames_bin[pointer:pointer + 10]
        frame_header = struct.unpack('>4sI2s', frame_header_bin)
        frame_body_size = frame_header[1]
        if frame_body_size == 0:
            break
        pointer += 10
        frames[frame_header[0]] = frames_bin[pointer:pointer + frame_body_size]
        pointer += frame_body_size
    TIT2_bin = frames.get(b'TIT2', None)
    TPE1_bin = frames.get(b'TPE1', None)
    TALB_bin = frames.get(b'TALB', None)

    if TALB_bin:
        encoding = encodings[TALB_bin[0]]
        frames[b'TALB'] = TALB_bin[1:].decode(encoding)
    if TIT2_bin:
        encoding = encodings[TIT2_bin[0]]
        frames[b'TIT2'] = TIT2_bin[1:].decode(encoding)
    if TPE1_bin:
        encoding = encodings[TPE1_bin[0]]
        frames[b'TPE1'] = TPE1_bin[1:].decode(encoding)
    return frames


def parse_ID3V2_head(head_bin):
    """
    获取数据头位置
    :param head_bin:
    :return:
    """
    if head_bin[:3] != b'ID3':
        return None
    frames_bin_size = (head_bin[6] << 21 | head_bin[7] << 14 |
                       head_bin[8] << 7 | head_bin[9])
    return frames_bin_size


def read_mp3_tag_v2():
    """
    :return:
    """
    f = open('D:/code/python/mp3/See You Again.128.mp3', 'rb')
    frames_bin_size = parse_ID3V2_head(f.read(10))
    if frames_bin_size is None:
        f.close()
        print('it not contain ID3V2')
        return
    frames_bin = f.read(frames_bin_size - 10)
    f.close()
    frames = parse_ID3V2_frames(frames_bin)
    tit2 = frames[b'TIT2']#标题
    print('标题：', tit2)
    tpe1 = frames[b'TPE1']#作者
    print('艺术家：',tpe1)
    talb = frames[b'TALB']#专辑
    print('专辑：', talb)
    pass


