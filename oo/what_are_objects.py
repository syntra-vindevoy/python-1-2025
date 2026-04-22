class Point:
    x: int = 0
    y: int = 0

    def print(self):
        print(self.x, self.y) #wat is self, het objectje gemaakt van mijn plannetje

    def calculate_distance(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

p1 = Point()

print(p1.x, p1.y)

p1.x = 10
p1.y = 20
print(p1.x, p1.y)
#p1.x = "toto" #geen fout
p1.z = 0 #geen fout
"""
class Person:
    last_name: str =""

p = Person()
p.lastname = "Doe"
"""
if type(p1) == Point:
    print("p1 is a point")
p2 = Point()
p2.x = 30
p2.y = 40

p1.print()

print(p1.calculate_distance(p2))

class Geometry: #utility class
    @classmethod #self wordt cls
    def calculate_distance(cls, p1: "Point", p2: "Point") -> float:
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

geo = Geometry()
#print(geo.calculate_distance(p1, p2))
print(Geometry.calculate_distance(p1,p2))
