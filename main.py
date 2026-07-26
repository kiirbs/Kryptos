from kryptos.chunk import Chunk
from kryptos.enums import ChunkType
        
chunk = Chunk(ChunkType.DATA, b"Hi")

print(ChunkType.DATA)
print(ChunkType.DATA.value)
print(ChunkType.DATA.name)

print(chunk.chunk_type)

print(chunk.content)