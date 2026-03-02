from datetime import date

class Person:       # Class is a blueprint, when creating an instances of the class  Class()  it's an object.
    name: str = ""
    date_of_birth: date = None

    @property   # Gebruikt om geen () te moeten gebruiken.  brent.age is natuurlijker dan  brent.age()
    def age(self) -> int:
        return (date.today() - self.date_of_birth).days // 356

brent = Person
brent.name = "Brent"
brent.date_of_birth = date(2000, 5, 8)
print(brent.age)

# *args     -> Argumenten zonder benamingen
# **kwargs  -> KeyWord Argumenten met benamingen