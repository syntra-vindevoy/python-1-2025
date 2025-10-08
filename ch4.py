from functools import partial
import turtle

def fun():
    bob = turtle.Turtle()
    bob.forward(100)
    bob.right(90)
    bob.forward(100)
    bob.circle(50)
    bob.left(90)
    bob.back(100)

    turtle.mainloop()

def penta(size):
    polygon(size=size, sides=5)

def circle(size):
    polygon(size=size, sides=360)

def polygon(size:int, sides:int):
    bob = turtle.Turtle()

    for i in range(sides):
        bob.forward(size)
        bob.right(360/sides)

    turtle.mainloop()

square = partial(polygon, sides=4)
pentagon = partial(polygon, sides=5)

def main():
    #HIER PROGRAMMEREN
    pentagon(100)

if __name__ == "__main__":
    main()