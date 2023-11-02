class tk:
    """
        Token class implementation
    """
    def __init__(self, types, value, line):
        self.type = types
        self.value = value
        self.line = line