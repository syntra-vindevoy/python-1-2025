class Animal:
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age

    def give_paw(self):
        print(self.name, "gave a paw")

class Dog(Animal):
    def bark(self):
        print(f"{self.name} says Woof!")

class Cat(Animal):
    def meow(self):
        print(f"{self.name} says Meow!")

blackie = Dog('Blackie',3)
musti = Cat('Musti', 2)

print(blackie.name, "is", blackie.age,"years old")
print(musti.name, "is", musti.age,"years old")

blackie.bark()
musti.meow()

blackie.give_paw()
musti.give_paw()
