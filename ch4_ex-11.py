from functools import partial
import turtle

from jupyturtle import make_turtle


# Exercise 1
def rectangle(side_horz:int, side_vert:int):
    parallelogram(side_horz=side_horz, side_vert=side_vert, angle= 90)

# Exercise 2
def rhombus(side_horz:int, side_vert:int, angle:int):
    parallelogram(side_horz=side_horz, side_vert=side_vert, angle= angle)

# Exercise 3
def parallelogram(side_horz:int, side_vert:int, angle:int):
    for i in range(2):
        turtle.forward(side_horz)
        turtle.left(angle)
        turtle.forward(side_vert)
        turtle.left(180-angle)

    turtle.mainloop()

def main():
    make_turtle()
    #rectangle(side_horz=80, side_vert=40)
    rhombus(side_horz=50, side_vert=50, angle=60)

if __name__ == "__main__":
    main()