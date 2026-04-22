class Contact:
    def __init__(self, name:str, email:str):
        self.name = name
        self.email = email

class Contacts:
    def __init__(self):
        self.contact = []

    def add(self, contact: Contact):
        self.contact.append(contact)

cc = Contacts()

robin = Contact("Robin","Robin@vorsselmans.net")

cc.add(robin)

#wat vind je het mooist? Er zijn verschillende design patterns. create contact ligt in factory design pattern.
# factory dp= je hebt een fabriek die iets maakt, maakt niet uit hoe, maar hij moet het terug geven. - vaak in loggers, best in naamgeving de factory erbij zetten, factry meethod sta ni in dit script
