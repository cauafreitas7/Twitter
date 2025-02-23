def gerador():
    id = 1
    while True:
        yield id
        id += 1
