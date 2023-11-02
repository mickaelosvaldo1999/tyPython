class Token:
    """
        Token class implementation
    """
    def __init__(self, types, value=None):
        self.types = types
        self.value = value
    
    def __str__(self):
        return f"<{self.types}, {self.value}>"