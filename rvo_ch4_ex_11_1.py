""" fast try to make all exercises, finish at home"""
import turtle

from numpy import number


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

def triangle(t, *, radius=100, angle=60):
    import math
    base = 2 * radius * math.sin(math.radians(angle / 2))
    equal_angle = (180 - angle) / 2

    t.right(angle / 2)
    t.forward(radius)
    t.left(180 - equal_angle)
    t.forward(base)
    t.left(180 - equal_angle)
    t.forward(radius)



def stacked_triangle(t, *, number=6, radius=100):
    angle = 360 / number
    for i in range(number):
        triangle(t, radius=radius, angle=angle)
        t.penup()
        t.home()
        t.pendown()
        t.right((i+1)*angle)

def polyline(t, n, length, angle):
 for i in range(n):
    t.forward(length)
    t.left(angle)

def arc(t, radius, angle):
    import math
    arc_length = 2 * math.pi * radius * angle / 360
    n = 30
    length = arc_length / n
    step_angle = angle / n
    polyline(t, n, length, step_angle)

def petal(t, radius, angle):
    arc(t, radius, angle)
    t.left(180-angle)
    arc(t, radius, angle)
def flower(t, radius, angle, leafs):
    for i in range(leafs):
        petal(t, radius, angle)
        t.penup()
        t.home()
        t.pendown()
        t.left((i+1)*(360/leafs))

def main():
    screen = turtle.Screen()
    t = turtle.Turtle()
    #rectangle(t)
    #rhombus(t)
    #   rectangle2(t)
    #rhombus2(t)
    #triangle(t,angle=72)
    #stacked_triangle(t, number=12)
    #arc(t, radius=100, angle=70)
    #petal(t,100,70)
    flower(t, 100,70,6)

if __name__ == '__main__':
    main()