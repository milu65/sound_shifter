import sound_shifter
import os

folder_path = 'test_audio_output'

if not os.path.exists(folder_path):
    os.makedirs(folder_path)


audio = sound_shifter.load("test_audio_files/blues.wav", "WAV")
sound_shifter.write("test_audio_output/wav2wav.wav", "WAV", audio)
sound_shifter.write("test_audio_output/wav2au.au", "AU", audio)
sound_shifter.write("test_audio_output/wav2aiff.aif", "AIFF", audio)

audio = sound_shifter.load("test_audio_files/M1F1-mulaw-AFsp.au", "AU")
sound_shifter.write("test_audio_output/au2au.au", "AU", audio)
sound_shifter.write("test_audio_output/au2wav.wav", "WAV", audio)
sound_shifter.write("test_audio_output/au2aiff.aif", "AIFF", audio)

audio = sound_shifter.load("test_audio_files/sample-3.aif", "AIFF")
sound_shifter.write("test_audio_output/aiff2aiff.aif", "AIFF", audio)
sound_shifter.write("test_audio_output/aiff2wav.wav", "WAV", audio)
sound_shifter.write("test_audio_output/aiff2au.au", "AU", audio)