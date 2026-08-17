from typing import Optional
from datetime import datetime

from kryptos.chunk import Chunk
from kryptos.field import Field
from kryptos.metadata_chunk import MetadataChunk
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
    
    def remove_chunk(self, chunk_type: enums.ChunkType):
        """Remove the chunk with the corresponding type."""
        
        for chunk in self.chunks:
            if chunk.chunk_type == chunk_type:
                self.chunks.remove(chunk)
                return
    
    def _set_metadata_field(self, field_type: enums.MetadataFieldType, value) -> None:
        
        if not isinstance(value, field_type.python_type):
            raise TypeError(
                f"{field_type.name} expects "
                f"{field_type.python_type.__name__}, "
                f"got {type(value).__name__}."
            )
        
        metadata = self.get_chunk(enums.ChunkType.METADATA)
            
        if metadata is None:
            metadata = MetadataChunk()
            self.add_chunk(metadata)
        
        field = metadata.get_field(field_type)
        
        if field is None:
            metadata.add_field(
                Field(field_type, value)
            )
        else:
            field.value = value
            
    def _get_metadata_field_value(self, field_type: enums.MetadataFieldType):
        
        metadata = self.get_chunk(enums.ChunkType.METADATA)
        
        if metadata is None:
            return None
        
        field = metadata.get_field(field_type)
        
        if field is None:
            return None
        
        return field.value
    
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
        
        encrypted, crypto_chunk = algorithm.encrypt(data_chunk.content)
        data_chunk.content = encrypted
        
        self.remove_chunk(enums.ChunkType.CRYPTO)
        
        if crypto_chunk is not None:
            self.add_chunk(crypto_chunk)
    
    def decrypt(self, key: bytes) -> None:
        
        if not self.validate():
            raise ValueError("Invalid file.")
        
        algorithm = self._get_algorithm(key)
        
        data_chunk = self.get_chunk(enums.ChunkType.DATA)
        assert data_chunk is not None
        
        crypto_chunk = self.get_chunk(enums.ChunkType.CRYPTO)
        
        data_chunk.content = algorithm.decrypt(
            data_chunk.content,
            crypto_chunk
        )
        
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
        
    def set_data(self, data: bytes) -> None:
        
        if not isinstance(data, bytes):
            raise TypeError("Expected bytes.")
        
        data_chunk = self.get_chunk(enums.ChunkType.DATA)
        
        if data_chunk is not None:
            data_chunk.content = data
        else:
            data_chunk = Chunk(enums.ChunkType.DATA, data)
            self.add_chunk(data_chunk)
            
    def get_data(self) -> bytes:
        
        data_chunk = self.get_chunk(enums.ChunkType.DATA)

        if data_chunk is None:
            raise ValueError("Missing data chunk.")

        return data_chunk.content
    
    def set_filename(self, value: str) -> None:
        self._set_metadata_field(enums.MetadataFieldType.ORIGINAL_FILENAME, value)
            
    def get_filename(self) -> Optional[str]:
        return self._get_metadata_field_value(enums.MetadataFieldType.ORIGINAL_FILENAME)
        
    def set_mime_type(self, value: str) -> None:
        self._set_metadata_field(enums.MetadataFieldType.MIME_TYPE, value)
        
    def get_mime_type(self) -> Optional[str]:
        return self._get_metadata_field_value(enums.MetadataFieldType.MIME_TYPE)
    
    def set_creation_timestamp(self, value: datetime) -> None:
        self._set_metadata_field(enums.MetadataFieldType.CREATION_TIMESTAMP, value)
            
    def get_creation_timestamp(self) -> Optional[datetime]:
        return self._get_metadata_field_value(enums.MetadataFieldType.CREATION_TIMESTAMP)
    
    def set_file_size(self, value: int) -> None:
        self._set_metadata_field(enums.MetadataFieldType.ORIGINAL_FILE_SIZE, value)
            
    def get_file_size(self) -> Optional[int]:
        return self._get_metadata_field_value(enums.MetadataFieldType.ORIGINAL_FILE_SIZE)
    
    def set_comment(self, value: str) -> None:
        self._set_metadata_field(enums.MetadataFieldType.COMMENT, value)
            
    def get_comment(self) -> Optional[str]:
        return self._get_metadata_field_value(enums.MetadataFieldType.COMMENT)