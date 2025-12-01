import turtle

# Setup
t = turtle.Turtle()
t.speed(5)
screen = turtle.Screen()
screen.bgcolor("skyblue")

# Function to draw a circle
def draw_circle(color, x, y, radius):
    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.fillcolor(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Draw Smurf body
draw_circle("blue", 0, -50, 50)  # body

# Draw Smurf head
draw_circle("blue", 0, 50, 40)  # head

# Draw Smurf hat
draw_circle("white", 0, 90, 40)

# Draw Smurf eyes
draw_circle("white", -15, 60, 10)  # left eye
draw_circle("white", 15, 60, 10)   # right eye
draw_circle("black", -15, 60, 5)   # left pupil
draw_circle("black", 15, 60, 5)    # right pupil

# Draw Smurf mouth
t.penup()
t.goto(-15, 40)
t.pendown()
t.right(90)
t.circle(15, 180)

# Draw Smurf pants
draw_circle("white", 0, -70, 30)  # pants

t.hideturtle()
turtle.done()
