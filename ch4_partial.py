from functools import partial
import turtle

def polygon(size: int, sides: int):
    """
    Draws a regular polygon using the Turtle graphics module.

    Each side of the polygon will have the specified length, and the polygon
    will have the specified number of sides.

    Parameters
    ----------
    size : int
        The length of each side of the polygon.
    sides : int
        The number of sides of the polygon.

    Returns
    -------
    None
        This function does not return anything. It draws the polygon using Turtle graphics.

    Examples
    --------
    >>> draw_polygon(100, 5)
    # Draws a regular pentagon with side length 100

    Author
    ------
    vindevoy

    Date
    ----
    2025-10-08
    """

    bob = turtle.Turtle()

    # vindevoy - 2025-10-08
    # A full circle is 360 degrees. We must turn those 360 degrees to complete the figure
    # So, on each side, we turn 360 degrees divided by the number of sides, which totals 360
    for i in range(sides):
        bob.forward(size)
        bob.left(360/sides)

# vindevoy
# This part did not work because ...
#    for jdksfqmjfkq
#        dsfdkjsqljfsq

    turtle.mainloop()

square = partial(polygon, sides=4)
pentagon = partial(polygon, sides=5)

def main():
    # polygon(100, 4)
    square(size=100)

if __name__ == '__main__':
    main()