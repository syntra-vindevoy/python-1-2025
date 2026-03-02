# class Contacts:
#     # def __init__(self):
#     #     self.contacts = []
#     #
#     # def add(self, contact: Contact):    # A type class is used for passing lots of data with class Settings for example.
#     #     self.contacts.append(contact)
#     #
#     # def create_contact(self, name:str, email: str):
#     #     c = Contact(name, email)
#     #     self.contacts.append(c)
#     #
#     #     return c # Returns contact again to see if contact adding has succeeded, and to use again for later.

class Contacts(list):
    pass

class Contact:
    def __init__(self, name:str, email:str):
        self.name = name
        self.age = email

cc = Contacts()

yves = Contact("Yves", "yves@vindevogel.net")
#cc.add(yves)
cc.append(yves)

print(yves)