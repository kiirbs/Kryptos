import unittest

from kryptos.metadata_chunk import MetadataChunk
from kryptos.field import Field
from kryptos.enums import ChunkType
from kryptos.enums import FieldType

"""
Unit tests for the Kryptos metadata chunk.
"""

class TestMetadataChunk(unittest.TestCase):
    
    def setUp(self):
        self.metadata = MetadataChunk()
    
    def _create_valid_field(
        self, 
        field_type=FieldType.ORIGINAL_FILENAME, 
        value="hello.txt"
    ) -> Field:
        return Field(
            field_type,
            value
        )
        
    def _build_filename_field(self) -> bytes:
        return (
            FieldType.ORIGINAL_FILENAME.field_id.to_bytes(1, "big")
            + (9).to_bytes(8, "big")
            + b"hello.txt"
        )
        
    def _build_size_field(self) -> bytes:
        return (
            FieldType.ORIGINAL_FILE_SIZE.field_id.to_bytes(1, "big")
            + (8).to_bytes(8, "big")
            + (12345).to_bytes(8, "big")
        )
    
    def _build_metadata(self, content: bytes) -> bytes:
        return (
            ChunkType.METADATA.value.to_bytes(1, "big") 
            + len(content).to_bytes(8, "big")
            + content
        )
    
    def test_add_field(self):
        
        self.metadata.add_field(self._create_valid_field())
        
        self.assertIsNotNone(
            self.metadata.get_field(FieldType.ORIGINAL_FILENAME)
        )
    
    def test_duplicate_field(self):
        
        with self.assertRaises(ValueError):
            self.metadata.add_field(self._create_valid_field())
            self.metadata.add_field(self._create_valid_field())
    
    def test_get_field(self):
        
        self.metadata.add_field(self._create_valid_field())
        
        field = self.metadata.get_field(FieldType.ORIGINAL_FILENAME)
        
        self.assertIsInstance(field, Field)
        
        self.assertIsNotNone(field)

        self.assertEqual(
            field.field_type,
            FieldType.ORIGINAL_FILENAME
        )

        self.assertEqual(
            field.value,
            "hello.txt"
        )
    
    def test_get_unknown_field(self):
        
        field = self.metadata.get_field(FieldType.COMMENT)
        
        self.assertIsNone(field)
    
    def test_serialize_empty_metadata(self):
        
        data = self.metadata.serialize()
        
        expected = (b"\x01" + (0).to_bytes(8, "big"))

        self.assertEqual(
            data,
            expected
        )
    
    def test_serialize_single_field(self):
        
        self.metadata.add_field(self._create_valid_field())
        
        data = self.metadata.serialize()
        
        expected_content = self._build_filename_field()
        
        expected = self._build_metadata(expected_content)
        
        self.assertEqual(
            data,
            expected
        )
    
    def test_serialize_multiple_fields(self):
        
        self.metadata.add_field(self._create_valid_field())
        self.metadata.add_field(self._create_valid_field(
            field_type=FieldType.ORIGINAL_FILE_SIZE,
            value=12345
        ))
        
        data = self.metadata.serialize()
        
        expected_content = (
            self._build_filename_field() 
            + self._build_size_field()
        )
        
        expected = self._build_metadata(expected_content)
        
        self.assertEqual(
            data,
            expected
        )