import numpy as np


def big_endian_bytes(value, length):
    return value.to_bytes(length, byteorder="big")


def write_header(file, header):
    file.write(header["magic"].encode("ascii"))
    file.write(big_endian_bytes(header["data_offset"], 4))
    file.write(big_endian_bytes(header["data_size"], 4))
    file.write(big_endian_bytes(header["encoding"], 4))
    file.write(big_endian_bytes(header["sample_rate"], 4))
    file.write(big_endian_bytes(header["channels"], 4))


def write_data(file, data):
    arr = data["data"].astype(np.uint8)
    for i in range(len(arr)):
        file.write(arr[i])


def write(filepath, chunks):
    with open(filepath, 'wb') as file:
        write_header(file, chunks[0])
        file.seek(chunks[0]["data_offset"], 0)
        write_data(file, chunks[1])
