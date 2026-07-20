def xor_bytes(data: bytes, key: int) -> bytes:
    """
    XOR each byte in the data with the given key.

    :param data: The input bytes to be XORed.
    :param key: The integer key to XOR with each byte.
    :return: A new bytes object with each byte XORed with the key.
    """
    if not 0 <= key <= 255:
        raise ValueError("Key must be an integer between 0 and 255.")
    
    return bytes(b ^ key for b in data)