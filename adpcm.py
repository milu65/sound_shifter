import array


def pcm_to_adpcm(pcm_data):
    indexTable = [-1, -1, -1, -1, 2, 4, 6, 8, -1, -1, -1, -1, 2, 4, 6, 8]
    stepsizeTable = [
        7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 25, 28, 31, 34, 37, 41, 45,
        50, 55, 60, 66, 73, 80, 88, 97, 107, 118, 130, 143, 157, 173, 190, 209, 230,
        253, 279, 307, 337, 371, 408, 449, 494, 544, 598, 658, 724, 796, 876, 963,
        1060, 1166, 1282, 1411, 1552, 1707, 1878, 2066, 2272, 2499, 2749, 3024, 3327,
        3660, 4026, 4428, 4871, 5358, 5894, 6484, 7132, 7845, 8630, 9493, 10442, 11487,
        12635, 13899, 15289, 16818, 18500, 20350, 22385, 24623, 27086, 29794, 32767
    ]

    output_buffer = 0
    buffer_step = True
    adpcm_data = array.array('h')

    # ADPCM encoding
    for i in range(0, len(pcm_data), 2):
        # val = struct.unpack('>h', pcm_data[i:i + 2])[0]
        val = pcm_data[i:i + 2][0][0].astype(int)
        diff = val
        sign = 0

        if diff < 0:
            sign = 8
            diff = -diff

        delta = 0
        vpdiff = stepsizeTable[output_buffer >> 3]

        if diff >= vpdiff:
            delta = 4
            diff -= vpdiff

        vpdiff >>= 1

        if diff >= vpdiff:
            delta |= 2
            diff -= vpdiff

        vpdiff >>= 1

        if diff >= vpdiff:
            delta |= 1

        if sign != 0:
            val = val - stepsizeTable[output_buffer >> 3]
        else:
            val = val + stepsizeTable[output_buffer >> 3]

        if val > 32767:
            val = 32767
        elif val < -32768:
            val = -32768

        delta |= sign
        index = output_buffer + indexTable[delta]

        if index < 0:
            index = 0
        elif index > 88:
            index = 88

        step = stepsizeTable[index]

        if buffer_step:
            output_buffer = delta & 0x0F
        else:
            adpcm_data.append(((delta << 4) & 0xF0) | output_buffer)
        buffer_step = not buffer_step

    return adpcm_data
