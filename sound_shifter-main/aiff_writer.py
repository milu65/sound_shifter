def write_audio(filepath, chunks):
    with open(filepath, 'wb') as file:
        write_chunk_form(file, chunks[0])
        write_chunk_comm(file, chunks[1])
        write_chunk_ssnd(file, chunks[2])


def write_chunk_form(file, chunk):
    file.write(chunk["chunk_name"].encode("ascii"))
    file.write(chunk["size"].to_bytes(4, "big"))
    file.write(chunk["type"].encode("ascii"))


def write_chunk_comm(file, chunk):
    file.write(chunk["chunk_name"].encode("ascii"))
    file.write(chunk["size"].to_bytes(4, "big"))
    file.write(chunk["num_channels"].to_bytes(2, "big"))
    file.write(chunk["sample_frames"].to_bytes(4, "big"))
    file.write(chunk["sample_size"].to_bytes(2, "big"))
    file.write(chunk["useless1"].to_bytes(2, "big"))
    file.write(chunk["sample_rate"].to_bytes(2, "big"))
    file.write(chunk["useless2"].to_bytes(6, "big"))


def write_chunk_ssnd(file, chunk):
    file.write(chunk["chunk_name"].encode("ascii"))
    file.write(chunk["size"].to_bytes(4, "big"))
    file.write(chunk["useless1"].to_bytes(4, "big"))
    file.write(chunk["useless2"].to_bytes(4, "big"))
    file.write(chunk["data"])
