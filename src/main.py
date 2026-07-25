from chunk import Chunk
from chunk_type import ChunkType
        
chunk = Chunk(ChunkType.DATA, b"Hi")

print(ChunkType.DATA)
print(ChunkType.DATA.value)
print(ChunkType.DATA.name)

print(chunk.chunk_type)

print(chunk.content)