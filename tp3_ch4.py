from functools import partial
import turtle

def fun():
    bob = turtle.Turtle()
    bob.forward(100)
    bob.right(90)
    bob.forward(100)
    bob.circle(50)
    bob.left(90)
    bob.back(100)

    turtle.mainloop()

def penta(size):
    polygon(size=size, sides=5)

def circle(size):
    polygon(size=size, sides=360)

def polygon(size:int, sides:int):
    # Dit is een manier van documentatie. Gebruik liever "numpy" voor een vorm van documentatie, zo krijg je die uitleg hier in pycharm als je over de functie staat met de muis.
    """
    This function creates a polygon with a given size and sides using a turtle.
    :param size: the length of the sides
    :param sides: the amount of sides
    :return: none
    :author: Brent Hendricx
    :date: 2025-10-08
    """
    bob = turtle.Turtle()

  # Het volgende is een voorbeeld van documenteren. Eerste regel is de persoon die het schreef en datum. Tweede regel en voort is de uitleg. Die uitleg is wat voor de hand liggend.
    # Brent Hendricx - 2025-10-08
    # A circle is 360 degrees, for calculating the angle you take the 360° and divide by the amount of corners.
    for i in range(sides):
        bob.forward(size)
        bob.right(360/sides)
  #Code die niet werkt, verwijder je niet weg en je zet er bij wat er niet werkte, waarom het niet werkte, en waarom het nu zo is.
    #Dit werkt. De while wait(1) werkte ook, maar dit wordt gebruikt enkel voor turtles en dus duidelijker.
    turtle.mainloop()

square = partial(polygon, sides=4)
pentagon = partial(polygon, sides=5)

def main():
    #HIER PROGRAMMEREN
    pentagon(100)

if __name__ == "__main__":
    main()