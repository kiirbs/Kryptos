from enum import Enum
from datetime import datetime

HEADER_SIZE = 8
DEFAULT_FLAGS = 0

CHUNK_TYPE_SIZE = 1
CHUNK_SIZE_FIELD_SIZE = 8

class ChunkType(Enum):
    METADATA = 0x01
    DATA = 0x02
    HASH = 0x03
    
class FieldType(Enum):        
    ORIGINAL_FILENAME = (0x01, str)
    MIME_TYPE = (0x02, str)
    CREATION_TIMESTAMP = (0x03, datetime)
    ORIGINAL_FILE_SIZE = (0x04, int)
    COMMENT = (0x05, str)
    
    def __init__(self, field_id, python_type):
        self.field_id = field_id
        self.python_type = python_type
    
class Version(Enum):
    V1 = 0x01
    
class Algo(Enum):
    XOR = 0x01
    
class MagicNumber(Enum):
    KPT1 = b"KPT1"