from toto import main
from toto import FIRST_NAME
from globals import APPLICATION_NAME

class Point:
    """Point class."""

    def __init__(self, x: int = 0, y: int = 0):
        """Point constructor."""

        self.x = x
        self.y = y

    def reset(self):
        self.x = 0
        self.y = 0

        return self

    def print(self):
        print(self.x, self.y)

        return self


p1 = Point()
p2 = Point()

p1.x = 10
p1.y = 20
p1.z = 40

p2.reset()

_ = p1.reset()

print(p1.x, p1.y)
print(p2.x, p2.y)

p1.reset().print()

p3 = Point(10, 20)
p4 = Point(y=10, x=20)

print(_.__dict__)

if __name__ == '__main__':
    print("I am a module")
