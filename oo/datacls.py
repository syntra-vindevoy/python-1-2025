from dataclasses import dataclass

@dataclass(slots=True)#als je die op true zet, kan je geen property definieren zoals hieronder
class person:
    name: str
    age: int

p = person("Robin",33)
#p.city="Merelbeke-Melle"


print(p)
#print(p.city)
#print(p.__dict__)