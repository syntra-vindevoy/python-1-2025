class Person:
    name: str = "Nobody"
    age: int = 0

p1 = Person()
p2 = Person()

p1.name = "John"

Person.age = 36

print(p2.name)
print(p2.age)
print(p1.age)

p3 = Person()
print(p3.age)

p1.age = 42

print(p1.age)
print(p2.age)
print(p3.age)
