def big_endian_ui(bytes):
    return int.from_bytes(bytes, "big")


def read_header(file):
    header = {}
    header["magic"] = file.read(4).decode("ascii")
    header["data_offset"] = big_endian_ui(file.read(4))
    header["data_size"] = big_endian_ui(file.read(4))
    header["encoding"] = big_endian_ui(file.read(4))
    header["sample_rate"] = big_endian_ui(file.read(4))
    header["channels"] = big_endian_ui(file.read(4))
    return header


def read_data(file, data_offset):
    data = {}
    file.seek(data_offset)
    data["data"] = file.read()
    return data


def read_audio(filepath):
    chunks = []
    with open(filepath, 'rb') as file:
        chunks.append(read_header(file))
        chunks.append(read_data(file,chunks[0]["data_offset"]))
    return chunks


path = 'test_audio_files/M1F1-mulaw-AFsp.au'
result = read_audio(path)
with open("au_output.txt", "w") as file:
    file.write(str(result))
