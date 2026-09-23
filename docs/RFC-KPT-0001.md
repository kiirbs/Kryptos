# RFC-KPT-0001
## Kryptos File Format

### 1. Status

Draft

---

### 2. Purpose

Define the format of `.kpt` files.

---

### 3. Scope

This RFC specifies the binary container format used by Kryptos `.kpt` files.

It defines:
- the file header;
- the chunk and field structures;
- the binary representation and serialization rules;
- the format dictionaries;
- the canonical chunk ordering;
- the object model of the file format;
- the cryptographic container requirements directly related to the `.kpt` format.

This RFC does not define:
- the Kryptos identity protocol;
- identity management and trust;
- event journal semantics;
- synchronization between machines;
- identity conflict resolution.

---

### 4. Design Principles

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

### 5. Terminology

| Term | Description |
|------|-------------|
| `Header` | Fixed bootstrap structure located at the beginning of the file. |
| `Chunk` | Self-contained binary block. |
| `Field` | Typed entry contained inside a field-based chunk. |

---

### 6. General Format Rules

- Each `ChunkType` may appear only once within the file.
- Each `MetadataFieldType` may appear only once within a `MetadataChunk`.
- Each `CryptoFieldType` may appear only once within a `CryptoChunk`.
- Metadata values are manipulated as native Python objects.
- Serialization and deserialization rules belong to `FieldType`.
- `Field` delegates binary conversion to its associated `FieldType`.
- `MetadataChunk` exposes a public API and hides its internal storage implementation.

---

### 7. Binary Specification

#### 7.1 General

| Chunk | Size | Description | State |
|-------|------|-------------|-------|
| Header | 8o | Bootstrap the parser | 🟢 OK | 
| Crypto | Variable | Cryptografy information | 🟢 OK |
| Metadata | Variable | Additional information | 🟢 OK |
| Encrypted Data | Variable | Content | 🟢 OK |
| Hash | Variable | Optional content fingerprint | 🟡 To be defined |

---

#### 7.2 Header

| Section | Size | Description | State | Endianness |
|---------|------|-------------|-------|------------|
| Magic Number | 4o | Format identifier | 🟢 OK | Yes |
| Version | 1o | Software Version | 🟢 OK | No |
| Header Size | 1o | Header size | 🟢 OK | No |
| Algorithm | 1o | Used algorithm | 🟢 OK | No |
| Flags | 1o | Bit flags | 🟡 To be defined | No |

---

#### 7.3 Chunks

| Section | Size | Description | State | Endianness |
|---------|------|-------------|-------|------------|
| Chunk Type | 1o | Chunk ID | 🟢 OK | No |
| Chunk Size | 8o | Chunk size | 🟢 OK | Yes |
| Content | Variable | Chunk content | 🟢 OK | Yes |

---

#### 7.4 Metadata & Crypto Fields

| Section | Size | Description | State | Endianness |
|---------|------|-------------|-------|------------|
| Field Type | 1o | Field ID | 🟢 OK | No |
| Field Size | 8o | Field size | 🟢 OK | Yes |
| Content | Variable | Field content | 🟢 OK | Yes |

---

### 8. Dictionaries

| Magic Number |
|--------------|
| `KPT1` |

| ID | Version |
|----|---------|
| 0x01 | V1 |

| ID | Algorithm |
|----|-----------|
| 0x01 | XOR |
| 0x02 | ChaCha20-Poly1305 |

| ID | Chunk Type |
|----|------------|
| 0x01 | Metadata |
| 0x02 | Encrypted data |
| 0x03 | Hash |
| 0x04 | Crypto |

| ID | Metadata Field Type | Type | Binary Repr | Serializer |
|----|---------------------|------|-------------|------------|
| 0x01 | Original Filename | `char` | UTF-8 | StringSerializer |
| 0x02 | MIME Type | `char` | UTF-8 | StringSerializer |
| 0x03 | Creation Timestamp | `datetime` | Unix timestamp (UInt64) | DatetimeSerializer |
| 0x04 | Original File Size | `int` | UInt64 | IntSerializer |
| 0x05 | Comment | `char` | UTF-8 | StringSerializer |

| ID | Crypto Field Type | Type | Representation | Role |
|----|-------------------|------|----------------|------|
| 0x01 | Nonce | `bytes` | 96 bits | Regenerate the encryption |
| 0x02 | Authentication Tag | `bytes` | 128 bits | Poly1305 verification |

---

### 9. Object Model

#### 9.1 Overview

```text
Fichier KPT
│
├── Header (bootstrap)
│
└── Chunks
    │
    ├── FieldChunk 
    │   │
    │   ├── Crypto
    │   │   └── CryptoFields
    │   │
    │   └── Metadata
    │       └── MetadataFields
    │
    ├── Data
    │
    └── Hash
```

```text
+------------------+
| Header           |
+------------------+
| Crypto Chunk     |
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

#### 9.2 Components

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
    └── FieldChunk
        ├── MetadataChunk
        │   │
        │   └── Field
        │           │
        │           └── MetadataFieldType
        └── CryptoChunk
            │
            └── Field
                    │
                    └── CryptoFieldType
```

---

#### 9.3 Responsibilities

- **`Header`**
    - Used to open and validate a Kryptos file.

- **`Chunk`**
    - Represents a single chunk.
    - Stores a `ChunkType`.

- **`ChunkType`**
    - Defines the different chunk types.

- **`MetadataFieldType`**
    - Defines a metadata field.
    - Stores its identifier.
    - Defines the expected Python type.
    - Handles serialization and deserialization.

- **`CryptoFieldType`**
    - Defines a crypto field.
    - Stores its identifier.
    - Defines the expected Python type.

- **`Field`**
    - Represents a typed field entry.
    - Stores a field descriptor and its value.
    - Validates the value.
    - Delegates serialization to its field descriptor.

- **`MetadataChunk`**
    - Stores all metadata fields.
    - Guarantees uniqueness of each `MetadataFieldType`.
    - Provides lookup, serialization, and size computation.

- **`CryptoChunk`**
    - Stores all crypto fields.
    - Guarantees uniqueness of each `CryptoFieldType`.
    - Provides lookup and size computation.
    - The Crypto Chunk is optional.
    - It MUST be present when required by the selected algorithm.
    - It MUST NOT be present when the selected algorithm does not require cryptographic parameters.

- **`NonceGenerator`**
    - generate() always returns exactly 12 bytes.
    - For a given persistent instance, the counter never decreases.
    - A counter that has already been used must never be reused.
    - The state must survive a reboot.
    - Two concurrent calls must never return the same nonce.
    - A clone or restore should not allow the reuse of space that has already been used.
    - The identifier is stable for a persistent instance.
    - For a given key, no nonce should be reused.

---

### 10. Cryptographic Rules

- **`ChaCha20-Poly1305`**:
    - 256 bits key
    - 96 bits nonce
    - 128 bits tag
    - AAD defined by Kryptos

- **Authentication / AAD**:
    - Privacy: ChaCha20
    - Authentication: Poly1305
    - AAD = serialized Header 
            || serialized Metadata Chunk(s) 
            || serialized Crypto Chunk without AUTH_TAG
            *(The canonical binary representation defined by KPT is used.)*

- **Hash Chunk**:
    - `HashChunk` is not used for cryptographic authentication; authenticated integrity is provided by ChaCha20-Poly1305.

---

### 11. Chunk Ordering

- The canonical chunk order is:
    - Header
    - Crypto
    - Metadata
    - Data
    - Hash

---

### 12. Invariants

- A file always begins with a header.
- The header is always 8 bytes long.
- All chunks have a type and a size.
- Multibyte integers are encoded in big-endian format.
- A chunk may be ignored if it is not recognized.
- For a fixed key, every encryption operation **MUST** use a unique 96-bit nonce.
- Kryptos implementations **MUST** use a nonce-generation mechanism that guarantees nonce uniqueness for a given key:
    - A nonce **MUST** be unique for every encryption using the same key.
    - Kryptos **MUST** generate a fresh unique nonce for each encryption performed with the same key.
- Each time a KPT file is encrypted, a new random session key is generated.
- `AUTH_TAG` **MUST** appear exactly once when using ChaCha20-Poly1305.
- `AUTH_TAG` **MUST NOT** be included in the AAD.
- The `AUTH_TAG` **MUST** be the final authentication tag produced for the complete authenticated message.
- Kryptos implementations **MUST** use a stateful nonce-generation strategy that guarantees this uniqueness.

---

## 13. Design Decisions

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

### 14. Future Extensions

Possible future extensions of the `.kpt` format include:

- additional cryptographic algorithms;
- additional metadata and crypto field types;
- additional chunk types;
- definition of the `Flags` field;
- additional integrity or fingerprint mechanisms;
- future format versions;
- optional protocol-specific chunks defined by other Kryptos RFCs.

These extensions are not part of the current specification and **MUST NOT**
be assumed to exist by implementations of the current version.

---