from time import time

from turtle import forward, left, right, back, mainloop

now = time()
print(now)

def recurse(n, s):
    if n == 0:
        print(s)
    else:
        recurse(n-1, n+s)

recurse(3, 0)


def draw(length):
    angle = 50
    factor = 0.6

    if length > 5:
        forward(length)
        left(angle)
        draw(factor * length)
        right(2 * angle)
        draw(factor * length)
        left(angle)
        back(length)

#draw(10)
#mainloop()


def koch(length):
    angle = 60

    if length > 5:
        forward(length/3)
        koch(length/3)
        left(angle)
        koch(length/3)
        forward(length/3)
        koch(length/3)
        right(2 * angle)
        koch(length/3)
        forward(length/3)
        koch(length/3)
        left(angle)
        koch(length/3)
        forward(length/3)
        koch(length/3)
    else:
        forward(length)

koch(60)
mainloop()