from kryptos.field_chunk import FieldChunk
from kryptos.enums import ChunkType

class CryptoChunk(FieldChunk):
    """Represents the crypto chunk of a Kryptos file."""
    
    def __init__(self):
        super().__init__(ChunkType.CRYPTO)