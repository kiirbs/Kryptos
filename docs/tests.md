# Tests listing

- **`Serializers`**:
    - [X] Round-trip
    - [X] Serialize invalid value
    - [X] Deserialize invalid value

- **`Chunk`**:
    - [X] Valid chunk
    - [X] Invalid content
    - [X] Serialize
    - [X] Size
    - [X] Representation

- **`MetadataChunk`**:
    - [X] Add field
    - [X] Duplicate field
    - [X] Get field
    - [X] Get unknow field
    - [X] Serialize empty metadata
    - [X] Serialize single field
    - [X] Serialize multiple fields

- **`Field`**:
    - [X] Valid field
    - [X] Serialize `str` field
    - [X] Serialize `int` field
    - [X] Serialize `datetime` field
    - [X] Invalid python type

- **`KryptosFile`**:
    - [X] Add chunk
    - [X] Duplicate chunk
    - [X] Get chunk
    - [X] Get unknow chunk
    - [X] Serialize without chunks
    - [X] Serialize invalid file
    - [X] Serialize valid file
    - [X] Encrypt decrypt valid file
    - [X] Encrypt invalid file
    - [X] Decrypt invalid file

- **`Parser`**:
    - [X] Magic Number
    - [X] Version
    - [X] Header Size
    - [X] Algo
    - [X] Valid file
    - [X] Unknow chunk type
    - [X] Duplicate data
    - [X] Duplicate metadata
    - [X] Missing hash
    - [X] Round-trip
    - [X] Unknow field type
    - [X] Corrupt metadata
    - [X] Truncated file

- **`Algorithm`**:
    - [X] Create valid algorithm
    - [X] Empty key
    - [X] Invalid key
    - [X] Encrypt invalid data
    - [X] Decrypt invalid data
    - [X] Encrypt valid data
    - [X] Round-trip

---