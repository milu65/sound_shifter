import numpy as np
import wav_reader
import au_writer
import wav_writer
import ulaw

chunks = wav_reader.read_chunks('test_audio_files/blues.wav')
pcm = chunks[2]['data']

# PCM data to frames (bits_per_sample=16)
pcm_data = np.frombuffer(pcm, dtype='<i2').reshape(-1, chunks[1]["num_channels"])

pcm_data = pcm_data.flatten()
ulaw_data = ulaw.encode(pcm_data)
header = {"magic": ".snd", "data_offset": 0x18,
          "data_size": len(ulaw_data), "encoding": 1,
          "sample_rate": chunks[1]["sample_rate"],
          "channels": chunks[1]["num_channels"],
          }
data = {"data": ulaw_data}
au_chunks = [header, data]
au_writer.write("test_audio_output/wav2au.au", au_chunks)


pcm_data_for_wav = ulaw.decode(ulaw_data)
chunks[2]['data'] = pcm_data_for_wav.astype(np.int16).tobytes()
wav_writer.write_audio("test_audio_output/wav2au2wav.wav", chunks)