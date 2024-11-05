# pylint: disable=redefined-builtin
# pylint: disable=invalid-name

class Tables:
    def __init__(self, id: int, name: str, token: str, columns: list) -> None:
        self.id = id
        self.name = name
        self.token = token
        self.columns = columns
