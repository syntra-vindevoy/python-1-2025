import math
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

def triangle_test(angle_point:float, height:int, test:float):
    turtle.forward(height)
    turtle.left(180-(180-angle_point)/2)
    #test = math.sqrt(math.pow(height, 2)+math.pow(a, 2))*2
    turtle.forward(math.sqrt(math.pow(height, 2) - math.pow(test, 2))*2)
    #turtle.forward(height²-test²=c²)
    turtle.left(180-(180-angle_point)/2)
    turtle.forward(height)
    turtle.left(180)

#def triangle_sss(height:int, side:int):
#def triangle_sas(height:int, side:int, angle:int):
def triangle_asa(height:int, angle_point:float, angle_twin:float):
    turtle.forward(height)
    turtle.left(angle_twin)
    turtle.forward(height)
    turtle.left(angle_twin)
    turtle.forward(height)
    turtle.left(180)
    """
    turtle.forward(height)
    #turtle.left(180-angle_twin*2)
    turtle.left(angle_twin)
    turtle.forward(height)
    #turtle.left(180-angle_twin*2)
    turtle.left(angle_twin)
    turtle.forward(height)
    turtle.left(180)
    """

def draw_pie(height:int, triangle_amount:int):
    for i in range(triangle_amount):
        triangle_asa(height=height, angle_point=360/triangle_amount, angle_twin=180-(360/triangle_amount))

def main():
    make_turtle()
    #rectangle(side_horz=80, side_vert=40)
    #rhombus(side_horz=50, side_vert=50, angle=60)
    #triangle_asa(height=80, angle_point=30, angle_twin=80)
    #draw_pie(height=80, draw_pie)
    triangle_test(angle_point=40, height=200, test=187.94)

    turtle.mainloop()

if __name__ == "__main__":
    main()