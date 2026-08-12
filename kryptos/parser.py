from typing import Tuple

from kryptos.kryptos_file import KryptosFile
from kryptos.header import Header
from kryptos.chunk import Chunk
from kryptos.metadata_chunk import MetadataChunk
from kryptos.field import Field
from kryptos import enums
from kryptos import exceptions

from kryptos.serializer import SERIALIZERS

class KryptosParser:
    """Represente the parser."""
    
    def _read_header(self, data: bytes) -> Header:
        
        magic = data[0:4]
        
        if magic != enums.MagicNumber.KPT1.value:
            raise exceptions.InvalidMagicNumberError()
        
        version = data[4]
        header_size = data[5]
        algo = data[6]
        flags = data[7]
        
        if header_size != 8:
            raise ValueError("Invalid header size.")
        
        magic = enums.MagicNumber(magic)
        version = enums.Version(version)
        algo = enums.Algo(algo)
        
        return Header(magic, version, header_size, algo, flags)
    
    def _read_field(self, data: bytes, cursor: int) -> Tuple[Field, int]:
        
        type_start = cursor
        size_start = type_start + enums.FIELD_TYPE_SIZE
        value_start = size_start + enums.FIELD_SIZE_FIELD_SIZE

        field_type = data[type_start]
        field_type = enums.FieldType.from_field_id(field_type)
        
        value_size = data[size_start:value_start]
        value_size = int.from_bytes(value_size, "big")
        
        serializer = SERIALIZERS[field_type.python_type]
        
        value_end = value_start + value_size
        value = data[value_start:value_end]
        value = serializer.deserialize(value)
        
        return Field(field_type, value), value_end
    
    def _read_metadata_chunk(
        self, 
        data: bytes, 
        content_start: int, 
        content_end: int
    ) -> MetadataChunk:
        
        metadata = MetadataChunk()
        
        field_cursor = content_start
        
        while field_cursor < content_end:
                        
            field, field_cursor = self._read_field(data, field_cursor)
                        
            metadata.add_field(field)
        
        return metadata
    
    def _read_chunk(self, data: bytes, cursor: int) -> Chunk:
        
        type_start = cursor
        size_start = type_start + enums.CHUNK_TYPE_SIZE
        content_start = size_start + enums.CHUNK_SIZE_FIELD_SIZE
        
        chunk_type = data[type_start]
        chunk_type = enums.ChunkType(chunk_type)
            
        content_size = data[size_start:content_start]
        content_size = int.from_bytes(content_size, "big")
        
        content_end = content_start + content_size
        
        if chunk_type == enums.ChunkType.METADATA:
            return self._read_metadata_chunk(
                data, 
                content_start, 
                content_end
            )
            
        content = data[content_start:content_end]
        
        return Chunk(chunk_type, content)
        
    def _add_chunks(self, cursor: int, kryptos_file: KryptosFile, data: bytes):
                
        while cursor < len(data):
            
            chunk = self._read_chunk(data, cursor)
            
            kryptos_file.add_chunk(chunk)
            
            chunk_size = (
                enums.CHUNK_TYPE_SIZE 
                + enums.CHUNK_SIZE_FIELD_SIZE 
                + chunk.size()
            )
            cursor += chunk_size
        
    def parse(self, data: bytes) -> KryptosFile:
        """Parses binary data into a KryptosFile."""
        
        header = self._read_header(data)
        
        cursor = header.header_size
        
        kryptos_file = KryptosFile()
        
        self._add_chunks(cursor, kryptos_file, data)
        
        if not kryptos_file.validate():
            raise ValueError("Invalid file.")
        
        return kryptos_file