from enum import Enum

HEADER_SIZE = 8
DEFAULT_FLAGS = 0

class ChunkType(Enum):
    METADATA = 0x01
    DATA = 0x02
    HASH = 0x03
    
class Version(Enum):
    V1 = 0x01
    
class Algo(Enum):
    XOR = 0x01
    
class MagicNumber(Enum):
    KPT1 = b"KPT1"
    
