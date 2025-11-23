import turtle

def koch(t,length):
    if length > 10:
        sublength = length/3
        koch(t, sublength)
        t.left(60)
        koch(t, sublength)
        t.right(120)
        koch(t, sublength)
        t.left(60)
        koch(t, sublength)
    else:
        t.forward(length)
        return

def main():
    t = turtle.Turtle()
    t.speed(0)
    koch(t, 1200)
if __name__ == '__main__':
    main()