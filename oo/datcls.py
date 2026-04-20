from dataclasses import dataclass

@dataclass(slots=True)
class Person():
    name: str
    age: int
    
p = Person("Yves", 53)


print(p)
