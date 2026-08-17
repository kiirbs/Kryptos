from typing import Optional

from kryptos.chunk import Chunk
from kryptos.field import FieldDescriptor, Field
from kryptos.enums import ChunkType

class FieldChunk(Chunk):
    """Represents the field chunk of a Kryptos file."""
    
    def __init__(self, chunk_type: ChunkType):
        
        super().__init__(chunk_type, b"")
        self.fields: dict[FieldDescriptor, Field] = {}
        
    def add_field(self, field: Field):
        """Add a field to the field chunk."""
        
        if field.field_type in self.fields:
            raise ValueError(f"Duplicate field: {field.field_type.name}.")
        
        self.fields[field.field_type] = field
        
    def get_field(self, field_type: FieldDescriptor) -> Optional[Field]:
        """Find the field with the corresponding type."""
        
        return self.fields.get(field_type)
    
    def size(self) -> int:
        """Return the size of the field chunk content."""
        
        return sum(field.size() for field in self.fields.values())
    
    def serialize(self) -> bytes:
        """Serialize the complete field chunk."""
        
        data = b""
        
        for field in self.fields.values():
            data += field.serialize()
            
        self.content = data
        
        return super().serialize()