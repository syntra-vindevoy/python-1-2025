class Animal:
    def __init__(self, name = "", age: int = 0):
        self.name = name
        self.age = age

    def give_paw(self):
        print(f"{self.name} gives a paw.")

class Dog(Animal):
    def bark(self):
        print(f"{self.name} says woof!")

class Cat(Animal):
    def meow(self):
        print(f"{self.name} says meow!")

def main():
    blacky = Dog("Blacky", 5)
    musti = Cat("Musti", 2)

    print(blacky.name, "is", blacky.age, "years old")
    print(musti.name, "is", musti.age, "years old")

    blacky.give_paw()
    musti.give_paw()
    blacky.bark()
    musti.meow()

if __name__ == '__main__':
    main()