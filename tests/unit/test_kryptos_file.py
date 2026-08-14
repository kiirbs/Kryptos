import unittest

from kryptos.kryptos_file import KryptosFile
from kryptos.chunk import Chunk
from kryptos.enums import ChunkType
from kryptos import enums

"""
Unit tests for the Kryptos file.
"""

class TestKryptosFile(unittest.TestCase):
    
    def setUp(self):
        self.file = KryptosFile()
        
    def _create_valid_chunk(
        self,
        chunk_type=ChunkType.DATA,
        content=b"Hello !"
    ):
        return Chunk(
            chunk_type,
            content
        )
    
    def test_add_chunk(self):
        
        self.file.add_chunk(self._create_valid_chunk())
        
        self.assertIsNotNone(
            self.file.get_chunk(ChunkType.DATA)
        )
        
    def test_duplicate_chunk(self):
        
        self.file.add_chunk(self._create_valid_chunk())
        self.file.add_chunk(self._create_valid_chunk())
        self.file.add_chunk(self._create_valid_chunk(
            chunk_type=ChunkType.HASH,
            content=b""
        ))
        
        with self.assertRaises(ValueError):
            self.file.serialize()
            
    def test_get_chunk(self):
        
        self.file.add_chunk(self._create_valid_chunk())
        
        chunk = self.file.get_chunk(ChunkType.DATA)
        
        self.assertIsNotNone(chunk)

        self.assertEqual(
            chunk.chunk_type,
            ChunkType.DATA
        )

        self.assertEqual(
            chunk.content,
            b"Hello !"
        )
        
    def test_get_unknown_chunk(self):
        
        field = self.file.get_chunk(ChunkType.HASH)
        
        self.assertIsNone(field)
        
    def test_serialize_without_chunks(self):
        
        with self.assertRaises(ValueError):
            self.file.serialize()
            
    def test_serialize_invalid_file(self):
        
        self.file.add_chunk(self._create_valid_chunk())
        
        with self.assertRaises(ValueError):
            self.file.serialize()
            
    def test_serialize_valid_file(self):
        
        self.file.add_chunk(self._create_valid_chunk())
        self.file.add_chunk(self._create_valid_chunk(
            chunk_type=ChunkType.HASH,
            content=b""
        ))
        
        data = self.file.serialize()
        
        expected = (
            enums.MagicNumber.KPT1.value
            + enums.Version.V1.value.to_bytes(1, "big")
            + enums.HEADER_SIZE.to_bytes(1, "big")
            + enums.Algo.XOR.value.to_bytes(1, "big")
            + enums.DEFAULT_FLAGS.to_bytes(1, "big")
            + ChunkType.DATA.value.to_bytes(1, "big")
            + (7).to_bytes(8, "big")
            + b"Hello !"
            + ChunkType.HASH.value.to_bytes(1, "big")
            + (0).to_bytes(8, "big")
            + b""
        )
        
        self.assertEqual(
            data,
            expected
        )
        
    def test_encrypt_decrypt_valid_file(self):
        
        data_chunk = self._create_valid_chunk()
        
        self.file.add_chunk(data_chunk)
        self.file.add_chunk(self._create_valid_chunk(
            chunk_type=ChunkType.HASH,
            content=b""
        ))
        
        original = data_chunk.content
        
        self.file.encrypt(b"key")

        self.assertNotEqual(original, data_chunk.content)

        self.file.decrypt(b"key")

        self.assertEqual(original, data_chunk.content)
        
    def test_encrypt_invalid_file(self):
        
        with self.assertRaises(ValueError):        
            self.file.encrypt(b"key")
                
    def test_decrypt_invalid_file(self):
        
        with self.assertRaises(ValueError):        
            self.file.decrypt(b"key")