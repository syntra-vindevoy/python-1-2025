from oo.inherr import DatabaseException


class ClientDatabaseException(DatabaseException):
    pass

class Client:
    def __init__(self, name: str):
        self.name = name

    def save(self):
        if self.name == "":
            raise ClientDatabaseException("Name cannot be empty")

