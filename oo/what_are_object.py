class Point:
    x: int = 0
    y: int = 0

    def print(self):    # Een klasse weet wat zichzelf is, self is een verwijzing naar zijn eigen.
        print("x:", self.x, "y:", self.y)

    def calculate_distance(self, other: "Point") -> float:  # "Point" en Point zijn geldig
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

p1 = Point()

print(p1.x)
print(p1.y)

p1.x = 10
p1.y = 20
print(p1.x)
print(p1.y)

p1.x = "toto"
print(p1.x) # -> Print accepteert elk type,
            # en in het proces dat van de waarde tot print geen check of verandering was, kon het doorgaan.

# Je kan een nieuwe variabel (doos) maken in het gemaakte object zoals bij een Dict. Het verandert de klasse (blueprint) niet.
p1.z = "nieuw"
print(p1.z)

# Zelfs een typefout kan een massale fout zijn
class Person:
    last_name: str = "_"
person1 = Person()
person1.lastname = "John"
print(person1.last_name)
print(person1.lastname)

# Elk gemaakt object is afzonderlijk van andere objecten, zelfs met hetzelfde type
p2 = Point()
p2.x = 100
print(p1.x) # Verandering in p1 zorgt niet voor een verandering p2

class Geometry:
    @classmethod #Zorgt ervoor dat je geen haakjes achter het oproepen van de klasse moet zetten
    def calculate_distance(self, pos1: Point, pos2: Point) -> float:
        return (pos1.x - pos2.x) ** 2 + (pos1.y - pos2.y) ** 2
geo_without_brackets = Geometry

geo = Geometry()
distance = geo.calculate_distance(p1, p2)
dist = Geometry().calculate_distance(p1, p2) # Werkt en is goed, maar maakt de klasse elke keer aan.
print(distance)
print(dist)