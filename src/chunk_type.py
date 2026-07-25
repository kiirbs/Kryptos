from enum import Enum

class ChunkType(Enum):
    METADATA = 0x01
    DATA = 0x02
    HASH = 0x03
    
