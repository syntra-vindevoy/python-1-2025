""" fast try to make all exercises, finish at home"""
import turtle


def rectangle(t, *,width = 80, height = 40):

    for i in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
def rhombus(t, *, length= 50, angle = 60):
    for i in range(2):
        t.forward(length)
        t.left(angle)
        t.forward(length)
        t.left(180-angle)
def parallelogram(t, *, width = 80, height = 40, angle = 90):
    for i in range(2):
        t.forward(width)
        t.left(angle)
        t.forward(height)
        t.left(180-angle)
def rectangle2(t, *,width = 80, height = 40):
    parallelogram(t, width=width, height=height, angle=90)

def rhombus2(t, *,width = 80, height = 40, angle = 60):
    parallelogram(t, width=width, height=height, angle=angle)

def triangle(t, *, sidelength = 50):
    for i in range(3):
        t.forward(sidelength)
        t.left(2/3*180)

def main():
    screen = turtle.Screen()
    t = turtle.Turtle()
    #rectangle(t)
    #rhombus(t)
    #   rectangle2(t)
    #rhombus2(t)
    triangle(t)

if __name__ == '__main__':
    main()