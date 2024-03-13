import numpy as np

import ulaw
import wav_reader
import wav_writer
import au_reader
import au_writer
import aiff_reader
import aiff_writer

import general_audio


def load(filepath, filetype):
    audio = None
    if filetype == 'WAV':  # TODO: num channels check
        chunks = wav_reader.read_chunks(filepath)
        data = np.frombuffer(chunks[2]['data'], dtype='<i2').reshape(-1, chunks[1]['num_channels'])
        audio = general_audio.GeneralAudio(chunks[1]['sample_rate'],
                                           chunks[1]['num_channels'],
                                           data)
    elif filetype == 'AU':
        chunks = au_reader.read_audio(filepath)
        data = np.frombuffer(chunks[1]['data'], dtype=np.int8).reshape(-1, chunks[0]['channels'])

        if chunks[0]['channels'] < 1:  # TODO: channels<1 check
            print("channels<1 ended")
            return audio

        col = ulaw.decode(data[:, 0])
        for i in range(1, chunks[0]['channels']):
            col = np.column_stack((col, ulaw.decode(data[:, i])))

        ulaw_decoded_data = col
        audio = general_audio.GeneralAudio(chunks[0]['sample_rate'],
                                           chunks[0]['channels'],
                                           ulaw_decoded_data)
    elif filetype == 'AIFF':
        chunks = aiff_reader.read_chunks(filepath)
        data = np.frombuffer(chunks[2]['data'], dtype='>i2').reshape(-1, chunks[1]['num_channels'])
        audio = general_audio.GeneralAudio(chunks[1]['sample_rate'],
                                           chunks[1]['num_channels'],
                                           data)
    else:
        print("unsupported file type", filetype)
    return audio


def write(filepath, filetype, audio):
    if filetype == 'WAV':
        data = audio.data.astype(np.int16).tobytes()
        bit_depth = 16
        wav_writer.write_audio(filepath, [
            {
                'chunk_name': 'RIFF',
                'size': 12 + 32 + len(data) - 8,  # 4 bytes
                'type': 'WAVE'
            },
            {
                'chunk_name': 'fmt ',
                'size': 16,  # 4 bytes
                'audio_format': 1,  # 2 bytes
                'num_channels': audio.num_channels,  # 2 bytes
                'sample_rate': audio.sample_rate,  # 4 bytes
                'byte_rate': int(audio.sample_rate * audio.num_channels * bit_depth / 8),  # 4 bytes
                'block_align': int((bit_depth / 8) * audio.num_channels),  # 2 bytes
                'bits_per_sample': bit_depth  # 2 bytes TODO: calc bits per sample
            },
            {
                'chunk_name': 'data',
                'size': len(data),  # 4 bytes
                'data': data
            }
        ])
    elif filetype == 'AU':
        if audio.num_channels < 1:  # TODO: channels<1 check
            print("channels<1 ended")
            return
        pcm_data = audio.data
        ulaw_data = ulaw.encode(pcm_data[:, 0])
        for i in range(1, audio.num_channels):
            ulaw_data = np.column_stack((ulaw_data, ulaw.encode(pcm_data[:, i])))
        header = {"magic": ".snd", "data_offset": 0x18,
                  "data_size": len(ulaw_data),
                  "encoding": 1,  # mu-law encoding
                  "sample_rate": audio.sample_rate,
                  "channels": audio.num_channels,
                  }
        data = {"data": ulaw_data}
        chunks = [header, data]
        au_writer.write(filepath, chunks)
    elif filetype == 'AIFF':
        data = audio.data.astype(np.int16).byteswap().tobytes()
        # data = audio.data
        # b= bytearray()
        # for i in range(len(audio.data)):
        #     for j in range(len(audio.data[i])):
        #         b.extend(audio.data[i][j].tobytes())
        bit_depth = 16
        aiff_writer.write_audio(filepath, [
            {
                'chunk_name': 'FORM',
                'size': len(data)+16+26+4,  # 4 bytes
                'type': 'AIFF'
            },
            {
                'chunk_name': 'COMM',
                'size': 18,  # 4 bytes
                'num_channels': audio.num_channels,  # 2 bytes
                "sample_frames":len(data)//(2*audio.num_channels),
                'sample_size': bit_depth,
                'useless1': 0x400e,
                'sample_rate': audio.sample_rate,  # 4 bytes
                'useless2': 0  
            },
            {
                'chunk_name': 'SSND',
                'size': len(data)+8,  # 4 bytes
                'useless1':0,
                'useless2':0,
                'data': data
            }
        ])
    else:
        print("unsupported file type", filetype)
