import math
import turtle


def polyline(t, n, length, angle):
    """Draws n line segments.

    t: Turtle object
    n: number of line segments
    length: length of each segment
    angle: degrees between segments
    """
    for i in range(n):
        t.fd(length)
        t.lt(angle)

def arc(t, r, angle):
    """Draws an arc with the given radius and angle.

    t: Turtle
    r: radius
    angle: angle subtended by the arc, in degrees
    """
    arc_length = 2 * math.pi * r * abs(angle) / 360
    n = int(arc_length / 4) + 3
    step_length = arc_length / n
    step_angle = float(angle) / n

    # making a slight left turn before starting reduces
    # the error caused by the linear approximation of the arc
    t.lt(step_angle/2)
    polyline(t, n, step_length, step_angle)
    t.rt(step_angle/2)

def leaf(t, r, angle):
    """Draws a leaf with the given radius and angle."""
    arc(t=t, r=r, angle=angle)
    t.lt(180 - angle)
    arc(t=t, r=r, angle=angle)

def flower_1(t):
    for i in range(7):
        leaf(t=t, r=300, angle=50)
        t.lt(180 / 7)

def flower_2(t):
    for i in range(9):
        leaf(t=t, r=200, angle=80)
        t.lt(180 / 9)

def main():
    t = turtle.Turtle()

    flower_1(t)

    turtle.mainloop()

if __name__ == "__main__":
    main()