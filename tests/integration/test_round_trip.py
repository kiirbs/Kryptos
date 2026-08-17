import unittest
from datetime import datetime

from kryptos.parser import KryptosParser
from kryptos.kryptos_file import KryptosFile
from kryptos.chunk import Chunk
from kryptos.metadata_chunk import MetadataChunk
from kryptos.field import Field
from kryptos.enums import MetadataFieldType
from kryptos.enums import ChunkType

"""
Complete round-trip test.
"""

TEST_VALUES = {
    str: "hello.txt",
    int: 12345,
    datetime: datetime(2026, 8, 5, 12, 0, 0)
}

class TestRoundTrip(unittest.TestCase):
    
    def _create_field(self, field_type, value) -> Field:
        return Field(field_type, value)
    
    def _create_metadata_chunk(self) -> MetadataChunk:
        
        metadata = MetadataChunk()
        
        for field in MetadataFieldType:
            value = TEST_VALUES[field.python_type]
            metadata.add_field(self._create_field(field, value))
            
        return metadata
    
    def _create_chunk(
        self, 
        chunk_type=ChunkType.HASH, 
        content=b""
    ) -> Chunk:
        if chunk_type == ChunkType.METADATA:
            return self._create_metadata_chunk()
        
        return Chunk(chunk_type, content)
    
    def test_round_trip(self):
        
        original = KryptosFile()
        original_content = b"This is my secret message !"
        
        data_chunk = self._create_chunk(chunk_type=ChunkType.DATA, content=original_content)
        
        original.add_chunk(self._create_chunk(chunk_type=ChunkType.METADATA))
        original.add_chunk(data_chunk)
        original.add_chunk(self._create_chunk())
        
        original.encrypt(b"key")
        
        binary = original.serialize()
                
        parsed = KryptosParser().parse(binary)
        
        parsed.decrypt(b"key")
        
        parsed_data = parsed.get_chunk(ChunkType.DATA)

        self.assertEqual(
            parsed_data.content,
            original_content
        )
        
        parsed.encrypt(b"key")
        
        binary2 = parsed.serialize()
        
        self.assertEqual(binary, binary2)