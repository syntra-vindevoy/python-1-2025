a = True

assert isinstance(a, int)
# assert type(a) == int

class Animal:
    pass

class Dog(Animal):
    pass

bob = Dog()
assert isinstance(bob, Dog)
assert isinstance(bob, Animal)

assert type(bob) is Dog
assert type(bob) is Animal