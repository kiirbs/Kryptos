from kryptos.field import Field
from kryptos.enums import MetadataFieldType
        
field = Field(MetadataFieldType.ORIGINAL_FILENAME, "hello.txt")
print(field.serialize())