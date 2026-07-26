from typing import Optional

from kryptos.chunk import Chunk
from kryptos import enums

class KryptosFile:
    
    def __init__(self):
        self.chunks = []
    
    def add_chunk(self, chunk: Chunk):
        self.chunks.append(chunk)
        
    def get_chunk(self, chunk_type: enums.ChunkType) -> Optional[Chunk]:
        
        for chunk in self.chunks:
            if chunk.chunk_type == chunk_type:
                return chunk
            
        return None
    
    def _count_chunks(self, chunk_type: enums.ChunkType) -> int:
        
        count = 0
        
        for chunk in self.chunks:
            count += (1 if chunk.chunk_type == chunk_type else 0)
            
        return count
    
    def _has_data_chunk(self):
        return self._count_chunks(enums.ChunkType.DATA) == 1
    
    def _has_hash_chunk(self):
        return self._count_chunks(enums.ChunkType.HASH) == 1
    
    def _metadata_is_valid(self):
        return self._count_chunks(enums.ChunkType.METADATA) <= 1
    
    def validate(self):
        return (
            self._has_data_chunk()
            and self._has_hash_chunk()
            and self._metadata_is_valid()
        )
        
    def serialize(self) -> bytes:
        if not self.validate():
            raise ValueError("File is not valide.")
            
        result = enums.MagicNumber.KPT1.value
        result += enums.Version.V1.value.to_bytes(1, "big")
        result += enums.HEADER_SIZE.to_bytes(1, "big")
        result += enums.Algo.XOR.value.to_bytes(1, "big")
        result += enums.DEFAULT_FLAGS.to_bytes(1, "big")
        
        for chunk in self.chunks:
            result += chunk.serialize()
        
        return result
        