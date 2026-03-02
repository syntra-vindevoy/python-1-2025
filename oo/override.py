class Animal:
    def __init__(self, name: str, age: int):
        self.name = name.capitalize()

        if age < 0:
            raise ValueError("Age must be positive")

        self.age = age

    @staticmethod
    def _eat(food: str):
        print(f"Animal eating {food}")


class Dog(Animal):
    def __init__(self, name: str, age: int, is_police_dog: bool = False):
        super().__init__(age=age, name=name)

        self.is_police_dog = is_police_dog

    def eat(self):
        super()._eat("brokskes")


class Cat(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(age=age, name=name)

    def eat(self):
        super()._eat("fish")


bobby = Dog("Bobby", 10, is_police_dog=True)
bobby.eat()

musti = Cat("Musti", 2)
musti.eat()

print(type(bobby))

if type(bobby) == Animal:
    print("Bobby is an animal")

if isinstance(bobby, Animal):
    print("Bobby is a animal")