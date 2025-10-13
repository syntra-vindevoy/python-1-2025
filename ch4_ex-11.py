from functools import partial
import turtle

from jupyturtle import make_turtle


# Exercise 1
def rectangle(side_horz:int, side_vert:int):
    for i in range(2):
        turtle.forward(side_horz)
        turtle.left(90)
        turtle.forward(side_vert)
        turtle.left(90)

    turtle.mainloop()

# Exercise 2
def rhombus(side:int, angle:int):
    for i in range(2):
        turtle.forward(side)
        turtle.left(angle)
        turtle.forward(side)
        turtle.left(180-angle)

    turtle.mainloop()

# Exercise 3
def parallelogram(side_horz:int, side_vert:int, angle:int):
    for i in range(2):
        turtle.forward(side_horz)
        turtle.left(angle)
        turtle.forward(side_vert)
        turtle.left(180-angle)

    turtle.mainloop()
rectangle_parl = partial(parallelogram,angle=90)
rhombus_parl = partial(parallelogram)

def main():
    make_turtle()
    #rectangle(side_horz=80, side_vert=40)
    #rhombus(side=50, angle=60)
    #rectangle_parl(side_horz=80, side_vert=40)
    rhombus_parl(side_horz=80, side_vert=40, angle=60)

if __name__ == "__main__":
    main()