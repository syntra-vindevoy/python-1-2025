class Contacts:
    def __init__(self):
        self.contacts = []

    def add(self, contact: Contact):
        self.contacts.append(contact)

    def create_contact(self, name: str, email: str):
        c = Contact(name, email)
        self.contacts.append(c)

        return c


class Contact:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

cc = Contacts()

yves = Contact("Yves", "yves@vindevogel.net")
cc.add(yves)

niels = cc.create_contact("Niels", "niels@vindevogel.net")
print(niels.name, niels.email)
