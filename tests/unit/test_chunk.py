import unittest

from kryptos.chunk import Chunk
from kryptos import enums

"""
Unit tests for Kryptos chunk.
"""

class TestChunk(unittest.TestCase):
    
    def test_create_valid_chunk(self):
        
        chunk = Chunk(enums.ChunkType.DATA, b"Hello !")
        
        self.assertEqual(chunk.chunk_type, enums.ChunkType.DATA)
        self.assertEqual(chunk.content, b"Hello !")
        
    def test_invalid_content(self):
        
        with self.assertRaises(TypeError):
            chunk = Chunk(enums.ChunkType.DATA, "Hello !")
            
    def test_serialize(self):
        
        chunk = Chunk(enums.ChunkType.DATA, b"Hello !")
        
        data = chunk.serialize()
        
        expected = (
            b"\x02"
            + (7).to_bytes(8, "big")
            + b"Hello !"
        )
        
        self.assertEqual(data, expected)
        
    def test_size(self):
        
        chunk = Chunk(enums.ChunkType.DATA, b"Hello !")
        
        chunk_size = chunk.size()
        
        expected = 7
        
        self.assertEqual(chunk_size, expected)
        
    def test_repr(self):
        
        chunk = Chunk(enums.ChunkType.DATA, b"Hello !")
        
        chunk_repr = repr(chunk)
        
        expected = (
            f"Chunk(\n"
            f"    type={enums.ChunkType.DATA.name}\n"
            f"    size={7}\n"
            f")"
        )
        
        self.assertEqual(chunk_repr, expected)