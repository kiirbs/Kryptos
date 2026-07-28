from kryptos.kryptos_file import KryptosFile
from kryptos.header import Header
from kryptos.chunk import Chunk
from kryptos import enums

class KryptosParser:
    
    def _read_header(self, data: bytes) -> Header:
        
        magic = data[0:4]
        
        if magic != enums.MagicNumber.KPT1.value:
            raise ValueError("Invalid magic number.")
        
        version = data[4]
        header_size = data[5]
        algo = data[6]
        flags = data[7]
        
        magic = enums.MagicNumber(magic)
        version = enums.Version(version)
        algo = enums.Algo(algo)
        
        return Header(magic, version, header_size, algo, flags)
    
    def _read_chunks(self, cursor, kryptos_file: KryptosFile, data: bytes):
                
        while cursor < len(data):
            
            type_start = cursor
            size_start = type_start + enums.CHUNK_TYPE_SIZE
            content_start = size_start + enums.CHUNK_SIZE_FIELD_SIZE
            
            chunk_type = data[type_start]
            chunk_type = enums.ChunkType(chunk_type)
            
            content_size = data[size_start:content_start]
            content_size = int.from_bytes(content_size, "big")
            
            content = data[content_start:(content_start+content_size)]
            
            kryptos_file.add_chunk(Chunk(chunk_type, content))
            
            cursor = content_start + content_size
        
    def parse(self, data: bytes) -> KryptosFile:
        
        header = self._read_header(data)
        
        cursor = header.header_size
        
        kryptos_file = KryptosFile()
        
        self._read_chunks(cursor, kryptos_file, data)
        
        kryptos_file.validate()
        
        return kryptos_file
    
    