import turtle
from turtle import forward, left, right, back, mainloop
import math

def triangle(length):
    for i in range(3):
        forward(length)
        left(120)

def draw_sierpinski(length:float, recursion:int):
    if recursion == 0: return

    triangle(length/2)
    forward(length/2)
    triangle(length/2)

    draw_sierpinski(length/2, recursion-1)

    left(120)
    forward(length/2)
    right(120)
    triangle(length/2)

    draw_sierpinski(length/2, recursion-1)

    left(60)
    back(length/2)
    right(60)

    draw_sierpinski(length/2, recursion-1)


def main():
    draw_sierpinski(100, 3)
    #triangle(100)
    mainloop()

if __name__ == "__main__":
    main()