def little_endian_ui(bytes):
    return int.from_bytes(bytes, "little")


def read_chunk_riff(file):
    riff = {}
    riff["size"] = little_endian_ui(file.read(4))
    riff["type"] = file.read(4).decode("ascii")
    return riff


def read_chunk_format(file):
    format = {}
    format["size"] = little_endian_ui(file.read(4))
    format["audio_format"] = little_endian_ui(file.read(2))
    format["num_channels"] = little_endian_ui(file.read(2))
    format["sample_rate"] = little_endian_ui(file.read(4))
    format["byte_rate"] = little_endian_ui(file.read(4))
    format["block_align"] = little_endian_ui(file.read(2))
    format["bits_per_sample"] = little_endian_ui(file.read(2))
    return format


def read_chunk_data(file):
    data = {}
    data["size"] = little_endian_ui(file.read(4))
    data["data"] = file.read(data["size"])
    return data


def read_chunks(filepath):
    chunks = []
    with open(filepath, 'rb') as file:
        while True:
            chunk_name = file.read(4)
            chunk_name = chunk_name.decode("ascii")
            if chunk_name == "RIFF":
                chunks.append(read_chunk_riff(file))
            elif chunk_name == "fmt ":
                chunks.append(read_chunk_format(file))
            elif chunk_name == "data":
                chunks.append(read_chunk_data(file))
            elif chunk_name == "":
                break
            else:
                print("unknow chunk name:", chunk_name)
                break
    return chunks


path = 'test_audio_files/blues.wav'
result = read_chunks(path)
with open("wav_output.txt", "w") as file:
    file.write(str(result))
