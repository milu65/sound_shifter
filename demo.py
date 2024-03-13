import sound_shifter

audio = sound_shifter.load("test_audio_files/blues.wav", "WAV")
sound_shifter.write("test_audio_output/wav2wav.wav", "WAV", audio)
sound_shifter.write("test_audio_output/wav2au.au", "AU", audio)

audio = sound_shifter.load("test_audio_files/M1F1-mulaw-AFsp.au", "AU")
sound_shifter.write("test_audio_output/au2au.au", "AU", audio)
sound_shifter.write("test_audio_output/au2wav.wav", "WAV", audio)