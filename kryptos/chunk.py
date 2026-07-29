from kryptos.enums import ChunkType

class Chunk:
    """Represents a single chunk inside a Kryptos file."""

    def __init__(self, chunk_type: ChunkType, content: bytes):
        
        self.chunk_type = chunk_type
        self.content = content
        
    def size(self):
        """Return the size of the chunk content."""
        
        return len(self.content)
        
    def serialize(self) -> bytes:
        """Serialize the chunk into its binary representation."""
        
        chunk_type = self.chunk_type.value.to_bytes(1, "big")
        chunk_size = self.size().to_bytes(8, "big")

        return chunk_type + chunk_size + self.content
    
    def __repr__(self):
        return (
            f"Chunk(\n"
            f"    type={self.chunk_type.name}\n"
            f"    size={self.size()}\n"
            f")"
        )