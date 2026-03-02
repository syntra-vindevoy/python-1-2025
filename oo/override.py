class Animal:
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age

    @staticmethod
    def _eat(food:str):
        print(f"Animal eating {food}")

class Dog(Animal):
    def __init__(self, name:str, age:int):
        super().__init__(age=age, name=name)

    def eat(self):
        super()._eat("food")

class Cat(Animal):
    def __init__(self, name:str, age:int):
        super().__init__(name=name, age=age)

    def eat(self):
        print("Cat eating...")

def main():
    animal = Animal()
    animal.eat()

    bobby = Dog()
    bobby.eat()

    musti = Cat()
    musti.eat()

    # If a methode is called through a class, then it searches in that class first.
    # If it has not been found, then it looks for the inherited class. Found, do that. Not, error.

if __name__ == "__main__":
    main()