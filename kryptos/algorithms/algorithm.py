from abc import ABC, abstractmethod
from typing import Optional

from kryptos.enums import Algo
from kryptos.crypto_chunk import CryptoChunk

class Algorithm(ABC):
    """Base class for all encryption algorithms."""

    def __init__(self, key: bytes):
        
        if not isinstance(key, bytes):
            raise TypeError("Expected bytes.")
        
        if len(key) == 0:
            raise ValueError("Key cannot be empty.")
        
        self.key = key
        
    @abstractmethod
    def encrypt(self, data: bytes) -> tuple[bytes, Optional[CryptoChunk]]:
        """Encrypt bytes."""
        ...
        
    @abstractmethod
    def decrypt(self, data: bytes, crypto_chunk: Optional[CryptoChunk]) -> bytes:
        """Decrypt bytes."""
        ...
        
class XORAlgorithm(Algorithm):
    
    def _xor(self, data: bytes) -> bytes:
        
        if not isinstance(data, bytes):
            raise TypeError("Expected bytes.")
        
        return bytes(
            b ^ self.key[i % len(self.key)] 
            for i, b in enumerate(data)
        )
    
    def encrypt(self, data: bytes) -> tuple[bytes, Optional[CryptoChunk]]:
        return self._xor(data), None
    
    def decrypt(self, data: bytes, crypto_chunk: Optional[CryptoChunk]) -> bytes:
        return self._xor(data)
    
ALGORITHMS = {
    Algo.XOR: XORAlgorithm,
}