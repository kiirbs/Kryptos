from kryptos.field_chunk import FieldChunk
from kryptos.enums import ChunkType

class MetadataChunk(FieldChunk):
    """Represents the metadata chunk of a Kryptos file."""
    
    def __init__(self):
        super().__init__(ChunkType.METADATA)