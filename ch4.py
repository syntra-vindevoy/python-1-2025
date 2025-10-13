import turtle

def polygon(size: int, sides: int):
    bob = turtle.Turtle()

    for i in range(sides):
        bob.forward(size)
        bob.left(360/sides)

    turtle.mainloop()

def square(size: int):
    polygon(size, 4)

def pentagon(size: int):
    polygon(size, 5)

def circle(size: int):
    polygon(size, 360)

def main():
    circle(2)

if __name__ == '__main__':
    main()