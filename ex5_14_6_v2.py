import turtle

def koch(t,length):
    if length < 10:
        t.forward(length)
        return
    sublength = length/3
    koch(t, sublength)
    t.left(60)
    koch(t, sublength)
    t.right(120)
    koch(t, sublength)
    t.left(60)
    koch(t, sublength)

def snowflake(t, n):
    """Draws a snowflake (a triangle with a Koch curve for each side)."""
    for i in range(3):
        koch(t, n)
        t.rt(120)

def main():
    t = turtle.Turtle()
    t.speed(0)
    #koch(t, 120)
    snowflake(t, 100)

if __name__ == '__main__':
    main()
