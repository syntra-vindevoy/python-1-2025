class Point:
    x: int = 0
    y: int = 0

    def print(self):
        print("x:", self.x, "y:", self.y)

    def calculate_distance(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

p1 = Point()

print(p1)
print(type(p1))

p1.print()

if type(p1) == Point:
    print("p1 is a Point")

print(p1.x)
print(p1.y)

p1.x = 10
p1.y = 20

print(p1.x)
print(p1.y)

p1.x = 10
p1.z = 0

print(p1.z)

p2 = Point()
p2.x = 100

print(p1.x)

print("the distance between p1 and p2 is", p1.calculate_distance(p2), "meters")


class Geometry:
    @classmethod
    def calculate_distance(cls, p1: Point, p2: Point) -> float:
        return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5

p3 = p1
p4 = p2

dist = Geometry.calculate_distance(p1, p2)
dist = Geometry.calculate_distance(p3, p4)

print(dist)

