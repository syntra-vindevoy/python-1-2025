class Animal:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def _eat(self, food):
        print(f"{self.name} is eating {food}")

class Dog(Animal):
    def __init__(self, name: str, age: int):
        super().__init__(name=name, age=age)

    def eat(self):
        super()._eat("Brokjes")

class Cat(Animal):
    def __init__(self, name:str, age:int):
        super().__init__(name=name, age=age) #init's the super first, waarom werkt dat omdat elke class een subobject van class Object is.
    def eat(self): #geeft ne warning!, omdat je een hogere eat overschrijft
        super()._eat("muizen")

bobbyDog = Dog("bobby", 12)
bobbyDog.eat()#gaat pas hoger kijken als er geen method is in de class
musti = Cat("musti",5)
#musti.eat() #werkt niet want je moet food meegegeven
musti.eat()

print(type(bobbyDog))

if type(bobbyDog) == Dog:
    print(f"{bobbyDog.name} is a dog")

if type(bobbyDog) == Animal:
    print(f"{bobbyDog.name} is an animal") #gaat niet werkenjom

if isinstance(bobbyDog, Animal): #houdt rekening met heel de klasse hierarchie
    print(f"{bobbyDog.name} is an animal, yo")
