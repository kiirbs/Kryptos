class Header:
    
    def __init__(
        self, 
        magic, 
        version, 
        header_size, 
        algo, 
        flags
    ):
        self.magic = magic
        self.version = version
        self.header_size = header_size
        self.algo = algo
        self.flags = flags