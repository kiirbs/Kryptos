import unittest

from kryptos.enums import Algo

from kryptos.algorithms.algorithm import ALGORITHMS

"""
Unit tests for Kryptos algorithms.
"""

class TestXORAlgorithm(unittest.TestCase):

    def setUp(self):
        self.algorithm_type = ALGORITHMS[Algo.XOR]
        
    def test_create_valid_algorithm(self):
        
        algorithm = self.algorithm_type(b"key")
        
        self.assertEqual(algorithm.key, b"key")
        
    def test_empty_key(self):
        
        with self.assertRaises(ValueError):
            algorithm = self.algorithm_type(b"")
            
    def test_invalid_key(self):
        
        with self.assertRaises(TypeError):
            algorithm = self.algorithm_type("key")
            
    def test_encrypt_invalid_data(self):
        
        algorithm = self.algorithm_type(b"key")
        
        with self.assertRaises(TypeError):
            cipher, crypto = algorithm.encrypt("Hello !")
            
    def test_decrypt_invalid_data(self):
        
        algorithm = self.algorithm_type(b"key")
        
        with self.assertRaises(TypeError):
            cipher, crypto = algorithm.decrypt("Hello !")
            
    def test_encrypt_valid_data(self):
        
        algorithm = self.algorithm_type(b"key")
        
        cipher, crypto = algorithm.encrypt(b"Hello !")
        
        self.assertIsNone(crypto)
        self.assertIsInstance(cipher, bytes)
        self.assertNotEqual(cipher, b"Hello !")
        
    def test_round_trip(self):
        
        algorithm = self.algorithm_type(b"key")
        
        plain = b"Hello Kryptos!"
        
        cipher, crypto = algorithm.encrypt(plain)
        
        result = algorithm.decrypt(cipher, crypto)
        
        self.assertIsNone(crypto)
        self.assertEqual(plain, result)