def read_chunks(filepath):
    chunks = []
    with open(filepath, 'rb') as file:
        chunks.append(read_chunk_form(file))
        chunks.append(read_chunk_comm(file))
        chunks.append(read_chunk_ssnd(file))
    return chunks

def read_chunk_form(file):
    form = {}
    chunk_name = file.read(4)
    chunk_name = chunk_name.decode("ascii")
    assert chunk_name == "FORM", print("unknow chunk name",chunk_name)
    form["chunk_name"] = chunk_name
    form["size"] =  int.from_bytes(file.read(4), byteorder='big')
    form["type"] = file.read(4).decode("ascii")
    return form


def read_chunk_comm(file):
    format = {}
    chunk_name = file.read(4)
    chunk_name = chunk_name.decode("ascii")
    assert chunk_name == "COMM", print("unknow chunk name",chunk_name)
    format["chunk_name"] = chunk_name
    format["size"] = int.from_bytes(file.read(4), byteorder='big')
    
    format["num_channels"] = int.from_bytes(file.read(2), byteorder='big')
    format["sample_frames"] = int.from_bytes(file.read(4), byteorder='big')
    format["sample_size"] = int.from_bytes(file.read(2), byteorder='big')
    file.read(2) #useless1
    format["sample_rate"] = int.from_bytes(file.read(2), byteorder='big')
    file.read(6) #useless2
    
    return format


def read_chunk_ssnd(file):
    data = {}
    chunk_name = file.read(4)
    chunk_name = chunk_name.decode("ascii")
    assert chunk_name == "SSND", print("unknow chunk name",chunk_name)
    data["chunk_name"] = chunk_name
    data["size"] = int.from_bytes(file.read(4), byteorder='big')
    data["offset"] = int.from_bytes(file.read(4), byteorder='big')
    data["block_size"] = int.from_bytes(file.read(4), byteorder='big')
    data["data"] = file.read(data["size"])
    return data
