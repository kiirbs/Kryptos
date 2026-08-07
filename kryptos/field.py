from kryptos.enums import FieldType
from kryptos.serializer import SERIALIZERS

class Field:
    """Represents a single field inside a MetadataChunk."""
    
    def __init__(self, field_type: FieldType, value):
        
        if not isinstance(value, field_type.python_type):
            raise TypeError(
                f"{field_type.name} expects "
                f"{field_type.python_type.__name__}, "
                f"got {type(value).__name__}."
            )
        
        self.field_type = field_type
        self.value = value
    
    def serialize(self) -> bytes:
        """Serialize the field into its binary representation."""
        
        serializer = SERIALIZERS[self.field_type.python_type]
        
        field_type = self.field_type.field_id.to_bytes(1, "big")
        data = serializer.serialize(self.value)
        field_size = len(data).to_bytes(8, "big")
        
        return field_type + field_size + data
    
    def size(self): 
        """Return the size of the field."""
               
        return len(self.serialize())
    
    def __repr__(self):
        return (
            f"Field(\n"
            f"    type={self.field_type.name}\n"
            f"    size={self.size()}\n"
            f"    value={self.value}\n"
            f")"
        )
        
        