from kryptos.field import Field
from kryptos.enums import FieldType
        
field = Field(FieldType.ORIGINAL_FILENAME, "hello.txt")
print(field.serialize())