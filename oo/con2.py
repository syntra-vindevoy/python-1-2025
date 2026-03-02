class Contacts(list):
    pass

class Contact:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

cc = Contacts()

yves = Contact("Yves", "yves@vindevogel.net")

cc.append(yves)

