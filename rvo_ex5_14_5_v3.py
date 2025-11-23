import turtle
from turtle import forward, left, right, back


def draw(length):
    angle = 50 #specify angle
    factor = 0.6 #specify some kind of factor
    t=turtle.Turtle() # custom alteration
    if length > 5: #if length is greater then 5 then execute  the following
        forward(length) #go forward the amount inputted
        left(angle) #turn 50 degrees left
        draw(factor * length) #draw 0,6 times length (this is recursive, so it will do this untill length is smaller than 5
        right(2 * angle) #turn back to original position and 50 degrees more to right
        draw(factor * length) #draw 0,6 times length (this is recursive, so it will do this until length is smaller than 5
        left(angle) # turn back to original position
        back(length) #go back

def main():
    draw(100)
if __name__ == '__main__':
    main()