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
    
    def _build_field(
        self,
        metadata_chunk_id=(0x01).to_bytes(1, "big"),
        metadata_chunk_size=(0x06).to_bytes(8, "big"),
        field_id=(0x01).to_bytes(1, "big"),
        field_size=(0x04).to_bytes(8, "big"),
        field_value=b"h.txt"
    ):
        return (
            metadata_chunk_id
            + metadata_chunk_size
            + field_id
            + field_size
            + field_value
        )
    
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
    
    def _build_file(self, header, chunks):
        return header + chunks
    
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
        
        valid_file = self._build_file(valid_header, valid_chunks)
        
        parsed = self.parser.parse(valid_file)
        
        data_chunk = parsed.get_chunk(enums.ChunkType.DATA)
        
        self.assertIsInstance(parsed, KryptosFile)
        
        self.assertIsNotNone(data_chunk)

        self.assertEqual(
            data_chunk.content,
            b"Hello !"
        )
        
    def test_unknown_chunk_type(self):
        
        valid_header = self._create_header()
        valid_chunks = self._build_chunks()
            
        fake_id = (0x99).to_bytes(1, "big")
        fake_size = (0x00).to_bytes(8, "big")
            
        fake_chunk = fake_id + fake_size
            
        invalid_file = self._build_file(valid_header, fake_chunk + valid_chunks)
        
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_file)
        
    def test_duplicate_data(self):
        
        valid_header = self._create_header()
        invalid_chunks = self._build_chunks(
            chunks=[
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
        )
        invalid_file = self._build_file(valid_header, invalid_chunks)
        
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_file)
            
    
    def test_duplicate_metadata(self):
        
        valid_header = self._create_header()
        invalid_chunks = self._build_chunks(
            chunks=[
                Chunk(enums.ChunkType.METADATA, b""),
                Chunk(enums.ChunkType.METADATA, b""),
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
        )
        invalid_file = self._build_file(valid_header, invalid_chunks)
        
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_file)
            
    def test_missing_hash(self):
        
        valid_header = self._create_header()
        invalid_chunks = self._build_chunks(
            chunks=[
                Chunk(enums.ChunkType.METADATA, b""),
                Chunk(enums.ChunkType.DATA, b"Hello !")
            ]
        )
        invalid_file = self._build_file(valid_header, invalid_chunks)
        
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_file)
    
    def test_unknown_field_type(self):
        
        valid_header = self._create_header()
        valid_chunks = self._build_chunks(
            chunks=[
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
        )
            
        fake_chunk = self._build_field(field_id=(0x99).to_bytes(1, "big"))
            
        invalid_file = self._build_file(valid_header, fake_chunk + valid_chunks)
        
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_file)
            
    def test_corrupt_metadata(self):
        
        valid_header = self._create_header()
        valid_chunks = self._build_chunks(
            chunks=[
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
        )
            
        fake_chunk = self._build_field(field_size=(0x00).to_bytes(8, "big"))
            
        invalid_file = self._build_file(valid_header, fake_chunk + valid_chunks)
        
        with self.assertRaises(ValueError):
            self.parser.parse(invalid_file)
            
    def test_truncated_file(self):
        
        valid_header = self._create_header()
        valid_chunks = self._build_chunks(
            chunks=[
                Chunk(enums.ChunkType.DATA, b"Hello !"),
                Chunk(enums.ChunkType.HASH, b"")
            ]
        )
        
        metadata_id = (0x01).to_bytes(1, "big")
        metadata_size = (0x99).to_bytes(8, "big")
        
        truncated_metadata = metadata_id + metadata_size
        
        truncated_file = self._build_file(valid_header, truncated_metadata + valid_chunks)
        
        with self.assertRaises(IndexError):
            self.parser.parse(truncated_file)