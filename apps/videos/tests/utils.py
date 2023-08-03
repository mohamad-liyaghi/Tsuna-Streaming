class FakeFile:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def _commited(self, **kwargs):
        return True
