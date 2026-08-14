from abc import ABC, abstractmethod

from kryptos.enums import Algo

class Algorithm(ABC):
    """Base class for all encryption algorithms."""

    def __init__(self, key: bytes):
        
        if not isinstance(key, bytes):
            raise TypeError("Expected bytes.")
        
        if len(key) == 0:
            raise ValueError("Key cannot be empty.")
        
        self.key = key
        
    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        """Encrypt bytes."""
        ...
        
    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        """Decrypt bytes."""
        ...
        
class XORAlgorithm(Algorithm):
    
    def encrypt(self, data: bytes) -> bytes:
        
        if not isinstance(data, bytes):
            raise TypeError("Expected bytes.")
        
        return bytes(
            b ^ self.key[i % len(self.key)] 
            for i, b in enumerate(data)
        )
    
    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)
    
ALGORITHMS = {
    Algo.XOR: XORAlgorithm,
}