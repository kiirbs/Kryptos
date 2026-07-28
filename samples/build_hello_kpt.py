from pathlib import Path

from kryptos.chunk import Chunk
from kryptos.kryptos_file import KryptosFile
from kryptos.enums import ChunkType

SAMPLES = Path("samples")

if __name__ == "__main__":
    
    with open(SAMPLES / "hello.txt", "rb") as f:
        data = f.read()
    
    data_chunk = Chunk(
        ChunkType.DATA,
        data
    )

    hash_chunk = Chunk(
        ChunkType.HASH,
        b""
    )

    kpt = KryptosFile()
    kpt.add_chunk(data_chunk)
    kpt.add_chunk(hash_chunk)

    binary = kpt.serialize()

    with open(SAMPLES / "hello.kpt", "wb") as f:
        f.write(binary)
        print(binary.hex(" "))
    
    print("Fichier Kryptos créé !")