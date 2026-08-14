from typing import Optional

from kryptos.chunk import Chunk
from kryptos import enums
from kryptos.algorithms.algorithm import Algorithm, ALGORITHMS

class KryptosFile:
    """Represents a Kryptos file."""
    
    def __init__(
        self, 
        version=enums.Version.V1, 
        algo=enums.Algo.XOR, 
        flags=0,
    ):
        self.version = version
        self.algo = algo
        self.flags = flags
        
        self.chunks = []
    
    def add_chunk(self, chunk: Chunk) -> None:
        """Add a chunk to the file."""
        
        self.chunks.append(chunk)
        
    def _get_algorithm(self, key: bytes) -> Algorithm:
        
        algorithm_class = ALGORITHMS[self.algo]
        
        return algorithm_class(key)
        
    def get_chunk(self, chunk_type: enums.ChunkType) -> Optional[Chunk]:
        """Find the chunk with the corresponding type."""
        
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
        
    def encrypt(self, key: bytes) -> None:
        
        if not self.validate():
            raise ValueError("Invalid file.")
        
        algorithm = self._get_algorithm(key)
        
        data_chunk = self.get_chunk(enums.ChunkType.DATA)
        assert data_chunk is not None
        
        data_chunk.content = algorithm.encrypt(data_chunk.content)
        
    def decrypt(self, key: bytes) -> None:
        
        if not self.validate():
            raise ValueError("Invalid file.")
        
        algorithm = self._get_algorithm(key)
        
        data_chunk = self.get_chunk(enums.ChunkType.DATA)
        assert data_chunk is not None
        
        data_chunk.content = algorithm.decrypt(data_chunk.content)
        
    def serialize(self) -> bytes:
        """Serialize the complete Kryptos file."""
        
        if not self.validate():
            raise ValueError("Invalid file.")
            
        result = enums.MagicNumber.KPT1.value
        result += self.version.value.to_bytes(1, "big")
        result += enums.HEADER_SIZE.to_bytes(1, "big")
        result += self.algo.value.to_bytes(1, "big")
        result += self.flags.to_bytes(1, "big")
        
        for chunk in self.chunks:
            result += chunk.serialize()
        
        return result
        