import unittest
from datetime import datetime

from kryptos.serializer import SERIALIZERS

"""
Unit tests for the Kryptos serializers.
"""

class TestStringSerializer(unittest.TestCase):
    
    def setUp(self):
        self.serializer = SERIALIZERS[str]
    
    def test_round_trip(self):
        
        value = "hello.txt"
        
        data = self.serializer.serialize(value)
        
        result = self.serializer.deserialize(data)

        self.assertEqual(data, b"hello.txt")
        self.assertEqual(result, value)

    def test_serialize_invalid_value(self):
      
        value = 12345

        with self.assertRaises(TypeError):
            self.serializer.serialize(value)
            
    def test_deserialize_invalid_value(self):
      
        value = 12345

        with self.assertRaises(TypeError):
            self.serializer.deserialize(value)

class TestUInt64Serializer(unittest.TestCase):
    
    def setUp(self):
        self.serializer = SERIALIZERS[int]

    def test_round_trip(self):
        
        value = 12345
        
        data = self.serializer.serialize(value)
        
        result = self.serializer.deserialize(data)

        self.assertEqual(data, value.to_bytes(8, "big"))
        self.assertEqual(result, value)
        
    def test_serialize_invalid_value(self):
      
        value = "hello.txt"

        with self.assertRaises(TypeError):
            self.serializer.serialize(value)
            
    def test_deserialize_invalid_value(self):
      
        value = "hello.txt"

        with self.assertRaises(TypeError):
            self.serializer.deserialize(value)

class TestUnixTimestampSerializer(unittest.TestCase):
    
    def setUp(self):
        self.serializer = SERIALIZERS[datetime]

    def test_round_trip(self):
        
        value = datetime(2026, 8, 5, 12, 0, 0)
        
        data = self.serializer.serialize(value)
        
        result = self.serializer.deserialize(data)

        self.assertEqual(data, (int(value.timestamp())).to_bytes(8, "big"))
        self.assertEqual(result, value)
        
    def test_serialize_invalid_value(self):
      
        value = "hello.txt"

        with self.assertRaises(TypeError):
            self.serializer.serialize(value)
            
    def test_deserialize_invalid_value(self):
      
        value = datetime(2026, 8, 5, 12, 0, 0)

        with self.assertRaises(TypeError):
            self.serializer.deserialize(value)