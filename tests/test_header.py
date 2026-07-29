import unittest

from kryptos.parser import KryptosParser
from kryptos import exceptions

"""
Unit tests for the Kryptos header.
"""
class TestHeader(unittest.TestCase):
    
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
        
        