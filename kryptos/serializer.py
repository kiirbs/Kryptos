from abc import ABC, abstractmethod
from datetime import datetime

class Serializer(ABC):
    """Base class for all serializers."""
    
    @abstractmethod
    def serialize(self, value):
        """Convert a Python object into bytes."""
        ...
    
    @abstractmethod
    def deserialize(self, data):
        """Convert bytes into a Python object."""
        ...

class StringSerializer(Serializer):
    
    def serialize(self, value: str) -> bytes:
        
        if not isinstance(value, str):
            raise TypeError("Expected a str.")
    
        return value.encode(encoding="utf-8")
    
    def deserialize(self, data: bytes) -> str:
        
        if not isinstance(data, bytes):
            raise TypeError("Expected bytes.")
        
        return data.decode('utf-8')

class UInt64Serializer(Serializer):
    
    def serialize(self, value: int) -> bytes:
        
        if not isinstance(value, int):
            raise TypeError("Expected an int.")
        
        return value.to_bytes(8, "big")
    
    def deserialize(self, data: bytes) -> int:
        
        if not isinstance(data, bytes):
            raise TypeError("Expected bytes.")
        
        return int.from_bytes(data, "big")
    
class UnixTimestampSerializer(Serializer):
    
    def __init__(self):
        self.uint64 = UInt64Serializer()
    
    def serialize(self, value: datetime) -> bytes:
        
        if not isinstance(value, datetime):
            raise TypeError("Expected a datetime.")
        
        return self.uint64.serialize(int(value.timestamp()))
    
    def deserialize(self, data: bytes) -> datetime:
        
        if not isinstance(data, bytes):
            raise TypeError("Expected bytes.")
        
        timestamp = self.uint64.deserialize(data)
        
        return datetime.fromtimestamp(timestamp)
    
SERIALIZERS = {
    str: StringSerializer(),
    int: UInt64Serializer(),
    datetime: UnixTimestampSerializer(),
}