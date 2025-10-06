# 3.11.3 Exercise
# Write a function called triangle that takes a string and an integer and draws a pyramid with the given height,
# made up using copies of the string. Here’s an example of a pyramid with 5 levels, using the string 'L'.
def triangle(brick:str = "=", length:int = 3):
    for i in range(length):
        print(brick * (i+1))

#----------------------------------------------------------------------------------------------------------------------------------
# 3.11.4 Exercise
# Write a function called rectangle that takes a string and two integers and draws a rectangle with the given width and height,
# made up using copies of the string. Here’s an example of a rectangle with width 5 and height 4, made up of the string 'H'.
def rectangle(brick:str = "=", width:int = 3, height:int = 3):
    for i in range(height):
        print(brick * width)

# ----------------------------------------------------------------------------------------------------------------------------------
# 3.11.5. Exercise
# The song “99 Bottles of Beer” automated by verse:
def bottle_verse(beers:int):
    if beers < 0: return    # Safety net

    for i in range(beers, 0, -1):
        print(f"{i} bottles of beer on the wall\n")
        if i == 0: return
        print(f"{i} bottles of beer\n"
              f"Take one down, pass it around\n")

# ----------------------------------------------------------------------------------------------------------------------------------
# Extra oef 1 (TP2_ch3_14.1)
# Write a function named right_justify that takes a string named s as a parameter and
# prints the string with enough leading spaces so that the last letter of the string is in column 70 of the display.
def right_justify(text:str):
    print(" " * (70 - len(text)) + text)

# ----------------------------------------------------------------------------------------------------------------------------------
# Extra oef 2 (TP2_ch3_14.2)
# A function object is a value you can assign to a variable or pass as an argument.
# For example, do_twice is a function that takes a function object as an argument and calls it twice:
def do_twice(f, value):
    f(value)
    f(value)

def do_four(f, value):
    do_twice(f, value)
    do_twice(f, value)

def print_spam(value):
    print(value)

# ----------------------------------------------------------------------------------------------------------------------------------
# Extra oef 3 (TP2_ch3_14.3) Note: This exercise should be done using only the statements and other features we
# have learned so far.
# 1. Write a function that draws a grid with lines of "-" and cross-section being "+"
print("+-----+-----+")
print("|     |     |")
print("|     |     |")
print("|     |     |")
print("|     |     |")
print("|     |     |")
print("+-----+-----+")
print("|     |     |")
print("|     |     |")
print("|     |     |")
print("|     |     |")
print("|     |     |")
print("+-----+-----+")
print()
print("*"*100)
print()

def horizontal_line_with_corners(squares:int, size:int, side:str, corner:str):
    for i in range(squares):
        print(corner, end="")
        if i >= squares-1: break
        print(side*(size-2), end="")
    print()
    return None

def vertical_line_without_corners(squares:int, size:int, side:str, filler:str):
    for i in range(size-2):
        for j in range(squares):
            print(side, end="")
            if j >= squares-1: break
            print((" " * len(filler)) * (size-2), end="")   # Tracht filler hier in te plaatsen om modulair te werken
        print()
    return None

def draw_grid(squares_size:int, squares_vert:int, squares_horz:int):
    corner = '+'
    side_vert = '|'
    side_horz = ' - '
    for i in range(squares_vert):
        horizontal_line_with_corners(squares=squares_horz, size=squares_size, side=side_horz, corner=corner)
        if i >= squares_horz: break
        vertical_line_without_corners(squares=squares_horz, size=squares_size, side=side_vert, filler=side_horz)
    horizontal_line_with_corners(squares=squares_horz, size=squares_size, corner=corner, side=side_horz)
    # for i in range(squares_horz):
    #     print(corner, end="")
    #
    #     for j in range(squares_size):
    #         print(side_horz, end="")
    #     print(corner)
    #
    #     for k in range(squares_vert):
    #         for l in range(squares_horz+1):
    #             print(side_vert, end="")
    #             for m in range(squares_size):
    #                 print(" ", end="")
    #         print()


# ----------------------------------------------------------------------------------------------------------------------------------
# Extra oef Yves
def repeated_call(func, number):
    for i in range(number):
        func()

def hello_world():
    repeated_call("Hello world", 3)

# ----------------------------------------------------------------------------------------------------------------------------------
def main():
    # triangle('L', 5)
    # rectangle('H', 5, 4)
    # bottle_verse(10)

    # right_justify('monty')
    # do_twice(print_spam, "spam")
    draw_grid(squares_size=5, squares_vert=2, squares_horz=7)

if __name__ == "__main__":
    main()