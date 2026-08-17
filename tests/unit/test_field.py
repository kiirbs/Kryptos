import unittest
from datetime import datetime

from kryptos.field import Field
from kryptos.enums import MetadataFieldType

"""
Unit tests for Kryptos fields.
"""

class TestField(unittest.TestCase):
    
    def test_create_valid_field(self):
        
        field = Field(MetadataFieldType.ORIGINAL_FILENAME, "hello.txt")
        
        self.assertEqual(field.field_type, MetadataFieldType.ORIGINAL_FILENAME)
        self.assertEqual(field.value, "hello.txt")
    
    def test_invalid_python_type(self):
        
        with self.assertRaises(TypeError):
            field = Field(MetadataFieldType.ORIGINAL_FILE_SIZE, "12345")
    
    def test_serialize_string_field(self):
        
        field = Field(MetadataFieldType.ORIGINAL_FILENAME, "hello.txt")
        
        data = field.serialize()
        
        expected = (
            b"\x01"
            + (9).to_bytes(8, "big")
            + b"hello.txt"
        )
        
        self.assertEqual(data, expected)
    
    def test_serialize_int_field(self):
        
        field = Field(MetadataFieldType.ORIGINAL_FILE_SIZE, 12345)
        
        data = field.serialize()
        
        expected = (
            b"\x04"
            + (8).to_bytes(8, "big")
            + (12345).to_bytes(8, "big")
        )
        
        self.assertEqual(data, expected)
    
    def test_serialize_datetime_field(self):
        
        field = Field(MetadataFieldType.CREATION_TIMESTAMP, datetime(2026, 8, 5, 12, 0, 0))
        
        data = field.serialize()
        
        expected = (
            b"\x03"
            + (8).to_bytes(8, "big")
            + (int(datetime(2026, 8, 5, 12, 0, 0).timestamp())).to_bytes(8, "big")
        )
        
        self.assertEqual(data, expected)