import unittest
from datetime import datetime

from kryptos.kryptos_file import KryptosFile
from kryptos import enums

class TestKryptosFileAPI(unittest.TestCase):
    
    def setUp(self):
        self.file = KryptosFile()
        
    def test_set_get_valid_data(self):
                
        self.file.set_data(b"Hello !")
        
        self.assertEqual(
            self.file.get_data(),
            b"Hello !"
        )        
        
    def test_set_invalid_data(self):
        
        with self.assertRaises(TypeError):
            self.file.set_data("Hello !")
            
    def test_set_get_valid_fields(self):
        
        self.file.set_filename("photo.png")
        self.file.set_mime_type("PHOTO/png")
        self.file.set_creation_timestamp(datetime(2026, 8, 5, 12, 0, 0))
        self.file.set_file_size(12345)
        self.file.set_comment("Vacances")
        
        self.assertEqual(
            self.file.get_filename(),
            "photo.png"
        )
        self.assertEqual(
            self.file.get_mime_type(),
            "PHOTO/png"
        )
        self.assertEqual(
            self.file.get_creation_timestamp(),
            datetime(2026, 8, 5, 12, 0, 0)
        )
        self.assertEqual(
            self.file.get_file_size(),
            12345
        )
        self.assertEqual(
            self.file.get_comment(),
            "Vacances"
        )
        
    def test_update_fields(self):
        
        self.file.set_filename("photo.png")
        self.file.set_mime_type("PHOTO/png")
        self.file.set_creation_timestamp(datetime(2026, 8, 5, 12, 0, 0))
        self.file.set_file_size(12345)
        self.file.set_comment("Vacances")
        
        self.file.set_filename("cat.jpg")
        self.file.set_mime_type("PHOTO/jpg")
        self.file.set_creation_timestamp(datetime(2024, 7, 2, 12, 0, 0))
        self.file.set_file_size(54321)
        self.file.set_comment("My cat")
        
        self.assertEqual(
            self.file.get_filename(),
            "cat.jpg"
        )
        self.assertEqual(
            self.file.get_mime_type(),
            "PHOTO/jpg"
        )
        self.assertEqual(
            self.file.get_creation_timestamp(),
            datetime(2024, 7, 2, 12, 0, 0)
        )
        self.assertEqual(
            self.file.get_file_size(),
            54321
        )
        self.assertEqual(
            self.file.get_comment(),
            "My cat"
        )
        
    def test_get_missing_fields(self):
        
        self.assertIsNone(
            self.file.get_filename()
        )
        self.assertIsNone(
            self.file.get_mime_type()
        )
        self.assertIsNone(
            self.file.get_creation_timestamp()
        )
        self.assertIsNone(
            self.file.get_file_size()
        )
        self.assertIsNone(
            self.file.get_comment()
        )
        
    def test_metadata_chunk_created_automatically(self):
        
        self.file.set_filename("photo.png")
        
        metadata = self.file.get_chunk(
            enums.ChunkType.METADATA
        )
        
        self.assertIsNotNone(metadata)
        
    def test_set_invalid_filename(self):

        with self.assertRaises(TypeError):
            self.file.set_filename(123)