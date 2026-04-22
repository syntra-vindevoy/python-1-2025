class Contact:
    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email

class Contacts(list):
    pass

cc = Contacts()

robin = Contact("Robin", "robin@vorsselmans.net")

cc.append(robin)

print(cc.__getitem__(0))