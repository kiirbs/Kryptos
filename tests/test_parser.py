import unittest

from kryptos.parser import KryptosParser
from kryptos.kryptos_file import KryptosFile
from kryptos.chunk import Chunk
from kryptos import enums

"""
Unit tests for the Kryptos parser.
"""

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = KryptosParser()
    
    def _build_binary(self, chunks=None) -> bytes:
        
        if chunks is None:
            chunks = [
                Chunk(enums.ChunkType.METADATA, b""),
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
        
        kpt_test = KryptosFile()
        
        for chunk in chunks:
            kpt_test.add_chunk(chunk)

        binary = kpt_test.serialize()
        
        return binary
            
    def test_valid_file(self):
        
        kpt_test = self._build_binary()
        
        parsed = self.parser.parse(kpt_test)
        
        data_chunk = parsed.get_chunk(enums.ChunkType.DATA)
        
        self.assertIsInstance(parsed, KryptosFile)
        
        self.assertIsNotNone(data_chunk)

        self.assertEqual(
            data_chunk.content,
            b"Hello !"
        )
        
    def test_unknow_chunk_type(self):
        
        with self.assertRaises(ValueError):
            kpt_test = self._build_binary()
            fake_id = (0x99).to_bytes(1, "big")
            fake_size = (0x00).to_bytes(8, "big")
            kpt_test += (fake_id + fake_size)
            self.parser.parse(kpt_test)
        
    def test_duplicate_data(self):
        
        with self.assertRaises(ValueError):
            kpt_test = self._build_binary(
                chunks=[
                    Chunk(enums.ChunkType.DATA, b"Hello !"),
                    Chunk(enums.ChunkType.DATA, b"Hello !"),
                    Chunk(enums.ChunkType.HASH, b"")
                ]
            )
            self.parser.parse(kpt_test)
            
    
    def test_duplicate_metadata(self):
        
        with self.assertRaises(ValueError):
            kpt_test = self._build_binary(
                chunks=[
                    Chunk(enums.ChunkType.METADATA, b""),
                    Chunk(enums.ChunkType.METADATA, b""),
                    Chunk(enums.ChunkType.DATA, b"Hello !"),
                    Chunk(enums.ChunkType.HASH, b"")
                ]
            )
            self.parser.parse(kpt_test)
            
    def test_missing_hash(self):
        
        with self.assertRaises(ValueError):
            kpt_test = self._build_binary(
                chunks=[
                    Chunk(enums.ChunkType.METADATA, b""),
                    Chunk(enums.ChunkType.DATA, b"Hello !")
                ]
            )
            self.parser.parse(kpt_test)