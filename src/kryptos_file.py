from chunk import Chunk
from chunk_type import ChunkType

class KriptosFile:
    
    def __init__(self):
        self.chunks = []
    
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)
        
    def get_chunk(self, chunk_type: ChunkType) -> Chunk | None:
        
        for chunk in self.chunks:
            if chunk.chunk_type == chunk_type:
                return chunk
            
        return None
    
    def _count_chunks(self, chunk_type: ChunkType) -> int:
        
        count = 0
        
        for chunk in self.chunks:
            count += (1 if chunk.chunk_type == chunk_type else 0)
            
        return count
    
    def _has_data_chunk(self):
        return self._count_chunks(ChunkType.DATA) == 1
    
    def _has_hash_chunk(self):
        return self._count_chunks(ChunkType.HASH) == 1
    
    def _metadata_is_valid(self):
        return self._count_chunks(ChunkType.METADATA) <= 1
    
    def validate(self):
        return (
            self._has_data_chunk()
            and self._has_hash_chunk()
            and self._metadata_is_valid()
        )