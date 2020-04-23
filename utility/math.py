def clamp_and_wrap(index, size):
    if index >= size:
        index = 0
    elif index < 0:
        index = size - 1
    return index
