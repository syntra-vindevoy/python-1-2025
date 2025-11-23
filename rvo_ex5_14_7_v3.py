import turtle


def sierpinski(t, length, depth):
    if depth == 0:
        # Draw an equilateral triangle
        for _ in range(3):
            t.forward(length)
            t.left(120)
    else:
        # Recursive subdivision
        sierpinski(t, length / 2, depth - 1)
        t.forward(length / 2)

        sierpinski(t, length / 2, depth - 1)
        t.backward(length / 2)
        t.left(60)
        t.forward(length / 2)
        t.right(60)

        sierpinski(t, length / 2, depth - 1)

        t.left(60)
        t.backward(length / 2)
        t.right(60)


def main():
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, -100)
    t.pendown()
    sierpinski(t, 400, 4)  # You can change depth here

    t.hideturtle()
    turtle.done()


if __name__ == "__main__":
    main()
