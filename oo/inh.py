class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def give_paw(self):
        print(self.name, "gave a paw.")

class Dog(Animal):
    def bark(self):
        print(f"{self.name} says Woof!")

class Cat(Animal):
    def meow(self):
        print(f"{self.name} says Meow!")

blacky = Dog("Blacky", 3)
musti = Cat("Musti", 2)

print(blacky.name, "is", blacky.age, "years old")
print(musti.name, "is", musti.age, "years old")

blacky.bark()
musti.meow()
blacky.give_paw()
musti.give_paw()