def write_little_endian_ui(number, length):
    return number.to_bytes(length, "little")


def write_chunk_riff(file, chunk):
    file.write(chunk["chunk_name"].encode("ascii"))
    file.write(write_little_endian_ui(chunk["size"], 4))
    file.write(chunk["type"].encode("ascii"))


def write_chunk_format(file, chunk):
    file.write(chunk["chunk_name"].encode("ascii"))
    file.write(write_little_endian_ui(chunk["size"], 4))
    file.write(write_little_endian_ui(chunk["audio_format"], 2))
    file.write(write_little_endian_ui(chunk["num_channels"], 2))
    file.write(write_little_endian_ui(chunk["sample_rate"], 4))
    file.write(write_little_endian_ui(chunk["byte_rate"], 4))
    file.write(write_little_endian_ui(chunk["block_align"], 2))
    file.write(write_little_endian_ui(chunk["bits_per_sample"], 2))


def write_chunk_data(file, chunk):
    file.write(chunk["chunk_name"].encode("ascii"))
    file.write(write_little_endian_ui(chunk["size"], 4))
    file.write(chunk["data"])


def write_audio(filepath, chunks):
    with open(filepath, 'wb') as file:
        write_chunk_riff(file, chunks[0])
        write_chunk_format(file, chunks[1])
        write_chunk_data(file, chunks[2])
