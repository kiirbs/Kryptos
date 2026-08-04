import unittest

from kryptos.parser import KryptosParser
from kryptos.kryptos_file import KryptosFile
from kryptos.chunk import Chunk
from kryptos import enums
from kryptos import exceptions

"""
Unit tests for the Kryptos parser.
"""

class TestParser(unittest.TestCase):
    
    def setUp(self):
        self.parser = KryptosParser()
        
    def _create_header(
        self,
        magic=b"KPT1",
        version=1,
        header_size=8,
        algo=1,
        flags=0
    ) -> bytes:
        return magic + bytes([version, header_size, algo, flags])
    
    def _build_chunks(self, chunks=None) -> bytes:
        
        if chunks is None:
            chunks = [
                Chunk(enums.ChunkType.METADATA, b""),
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
                
        data = b""
        
        for chunk in chunks:
            data += chunk.serialize()
        
        return data
    
    def test_invalid_magic_number(self):
        
        data = self._create_header(magic=b"ABCD")
                
        with self.assertRaises(exceptions.InvalidMagicNumberError):
            self.parser.parse(data)
            
    def test_invalid_version(self):
        
        data = self._create_header(version=99)
        
        with self.assertRaises(ValueError):
            self.parser.parse(data)
            
    def test_invalid_header_size(self):
        
        data = self._create_header(header_size=99)
        
        with self.assertRaises(ValueError):
            self.parser.parse(data)
            
    def test_invalid_algo(self):
        
        data = self._create_header(algo=99)
        
        with self.assertRaises(ValueError):
            self.parser.parse(data)
            
    def test_valid_file(self):
        
        valid_header = self._create_header()
        valid_chunks = self._build_chunks()
        
        valid_file = valid_header + valid_chunks
        
        parsed = self.parser.parse(valid_file)
        
        data_chunk = parsed.get_chunk(enums.ChunkType.DATA)
        
        self.assertIsInstance(parsed, KryptosFile)
        
        self.assertIsNotNone(data_chunk)

        self.assertEqual(
            data_chunk.content,
            b"Hello !"
        )
        
    def test_unknow_chunk_type(self):
        
        with self.assertRaises(ValueError):
            
            valid_header = self._create_header()
            valid_chunks = self._build_chunks()
            
            fake_id = (0x99).to_bytes(1, "big")
            fake_size = (0x00).to_bytes(8, "big")
            
            fake_chunk = fake_id + fake_size
            
            invalid_file = valid_header + fake_chunk + valid_chunks
            
            self.parser.parse(invalid_file)
        
    def test_duplicate_data(self):
        
        with self.assertRaises(ValueError):
            valid_header = self._create_header()
            invalid_chunks = self._build_chunks(
                chunks=[
                    Chunk(enums.ChunkType.DATA, b"Hello !"),
                    Chunk(enums.ChunkType.DATA, b"Hello !"),
                    Chunk(enums.ChunkType.HASH, b"")
                ]
            )
            invalid_file = valid_header + invalid_chunks
            self.parser.parse(invalid_file)
            
    
    def test_duplicate_metadata(self):
        
        with self.assertRaises(ValueError):
            valid_header = self._create_header()
            invalid_chunks = self._build_chunks(
                chunks=[
                    Chunk(enums.ChunkType.METADATA, b""),
                    Chunk(enums.ChunkType.METADATA, b""),
                    Chunk(enums.ChunkType.DATA, b"Hello !"),
                    Chunk(enums.ChunkType.HASH, b"")
                ]
            )
            invalid_file = valid_header + invalid_chunks
            self.parser.parse(invalid_file)
            
    def test_missing_hash(self):
        
        with self.assertRaises(ValueError):
            valid_header = self._create_header()
            invalid_chunks = self._build_chunks(
                chunks=[
                    Chunk(enums.ChunkType.METADATA, b""),
                    Chunk(enums.ChunkType.DATA, b"Hello !")
                ]
            )
            invalid_file = valid_header + invalid_chunks
            self.parser.parse(invalid_file)