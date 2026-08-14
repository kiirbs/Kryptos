from typing import Optional

from kryptos.chunk import Chunk
from kryptos.field import Field
from kryptos.enums import ChunkType, FieldType

class MetadataChunk(Chunk):
    """Represents the metadata chunk of a Kryptos file."""
    
    def __init__(self):
        
        super().__init__(ChunkType.METADATA, b"")
        self.fields: dict[FieldType, Field] = {}
        
    def add_field(self, field: Field):
        """Add a field to the metadata chunk."""
        
        if field.field_type in self.fields:
            raise ValueError(f"Duplicate field: {field.field_type.name}.")
        
        self.fields[field.field_type] = field
        
    def get_field(self, field_type: FieldType) -> Optional[Field]:
        """Find the field with the corresponding type."""
        
        return self.fields.get(field_type)
    
    def size(self):
        """Return the size of the metadata chunk content."""
        
        return sum(field.size() for field in self.fields.values())
    
    def serialize(self) -> bytes:
        """Serialize the complete metadata chunk."""
        
        data = b""
        
        for field in self.fields.values():
            data += field.serialize()
            
        self.content = data
        
        return super().serialize()