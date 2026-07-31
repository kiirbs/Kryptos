# RFC-KPT-0001
## Format de fichier Kryptos

### Statut

Draft

---

## Purpose

Define the format of `.kpt` files.

---

## Design Principles

- Extensible format
- Minimal header
- Independent chunks
- No redundant information
- Upward compatibility
- Separation of concerns
- Downward compatibility where possible
- Avoid inferable information
- Objects represent the concepts in the specification

---

## Invariants

- A file always begins with a header
- The header is always 8 bytes long
- All chunks have a type and a size
- Multibyte integers are encoded in big-endian format
- A chunk may be ignored if it is not recognized

---

## Terminology

| Term | Description |
|------|-------------|
| Header | Fixed bootstrap structure located at the beginning of the file. |
| Chunk | Self-contained binary block. |
| Field | Metadata entry contained inside the Metadata Chunk. |

---

## Binary Specification

### General

| Chunk | Size | Description | State |
|-------|------|-------------|-------|
| Header | 8o | Bootstrap the parser | 🟢 OK | 
| Metadata | Variable | Additional Information | 🟢 OK |
| Encrypted Data | Variable | Content | 🟢 OK |
| Hash | Variable | Integrity Check | 🟡 To be determined |

---

### Header

| Section | Size | Description | State | Endianness |
|---------|------|-------------|-------|------------|
| Magic Number | 4o | Format identifier | 🟢 OK | Yes |
| Version | 1o | Software Version | 🟢 OK | No |
| Header Size | 1o | Header size | 🟢 OK | No |
| Algorithm | 1o | Used algorithm | 🟢 OK | No |
| Flags | 1o | Bit flags | 🟡 To be determined | No |

---

### Chunks

| Section | Size | Description | State | Endianness |
|---------|------|-------------|-------|------------|
| Chunk Type | 1o | Chunk ID | 🟢 OK | No |
| Chunk Size | 8o | Chunk size | 🟢 OK | Yes |
| Content | Variable | Chunk content | 🟢 OK | Yes |

---

### Metadata Fields

| Section | Size | Description | State | Endianness |
|---------|------|-------------|-------|------------|
| Field Type | 1o | Field ID | 🟢 OK | No |
| Field Size | 8o | Field size | 🟢 OK | Yes |
| Content | Variable | Field content | 🟢 OK | Yes |

---

### Dictionaries

| Magic Number |
|--------------|
| `KPT1` |

| ID | Version |
|----|---------|
| 0x01 | V1 |

| ID | Algorithm |
|----|-----------|
| 0x01 | XOR |

| ID | Chunk Type |
|----|------------|
| 0x01 | Metadata |
| 0x02 | Encrypted data |
| 0x03 | Hash |

| ID | Field Type | Type | Description |
|----|------------|------|-------------|
| 0x01 | Original Filename | `char` | Restore the original name |
| 0x02 | MIME Type | `char` | Knowing what type of file you're decrypting |
| 0x03 | Creation Timestamp | `datetime` | Keep the creation date |
| 0x04 | Original File Size | `int` | Verification and Restoration |
| 0x05 | Comment | `char` | Leave an optional note |

---

## Object Model

### Overview

```text
Fichier KPT
│
├── Header (bootstrap)
│
└── Chunks
    │
    ├── Metadata
    │   └── Fields
    │
    ├── Data
    │
    └── Hash
```

```text
+------------------+
| Header           |
+------------------+
| Metadata Chunk   |
+------------------+
| Data Chunk       |
+------------------+
| Hash Chunk       |
+------------------+
```

```text
Chunk

+------+----------+-----------+
| Type | Size (8) | Content   |
+------+----------+-----------+
```

---

### Components

```text
Reference Object Model

KryptosFile
│
├── Header
│
└── Chunk
    │
    ├── DataChunk
    ├── HashChunk
    └── MetadataChunk
            │
            └── Field
                    │
                    └── FieldType
```

---

### Reference Components

│ Component │ Responsibilitie │
│-----------│-----------------│
│ `Header` │ Used to open and view the file properly. │
│ `Chunk` │ Represents a single chunk. Stores a `ChunksType` value. │
│ `ChunksType` │ Define differents types of chunks. │
│ `FieldType` │ Defines a metadata field. Stores its identifier, expected Python type and serialization/deserialization rules. │
│ `Field` │ Represents a single metadata entry. Stores a `FieldType` and its associated value. Validates the value and delegates serialization to the `FieldType`. │
│ `MetadataChunk` │ Stores all metadata fields of a Kryptos file. Guarantees uniqueness of each `FieldType` and provides access, serialization and size computation. │

---

### Design Principles

- Each `ChunkType` may appear only once within the file.
- Each `FieldType` may appear only once within a `MetadataChunk`.
- Metadata values are manipulated as native Python objects.
- Serialization and deserialization rules belong to `FieldType`.
- `Field` delegates binary conversion to its associated `FieldType`.
- `MetadataChunk` exposes a public API and hides its internal storage implementation.

---

## Design Decisions

- Fixed-size header
    - Fast read
    - Compatible with future versions
    - Stable structure

- Optional metadata
    - Privacy protection
    - Reduced file size
    - Flexibility

- Algorithms represented by a numeric identifier
    - Compact format
    - Fast read
    - Extensible

- The `.kpt` format is a block-oriented binary container
    - It consists of:
        - A fixed 8-byte header
        - A sequence of independent blocks
    - Each block has:
        - An identifier
        - A size
        - Content
    - Advantages:
        - Extensible
        - Single point of responsibility
        - Simple

- Big-endian implementation
    - Readable
    - Simple
    - Widely used

- Recursive architecture
    - Modular

---