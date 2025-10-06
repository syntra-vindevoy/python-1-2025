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
# Extra oef 1 (TP2_ch3_14.1
# Write a function named right_justify that takes a string named s as a parameter and
# prints the string with enough leading spaces so that the last letter of the string is in column 70 of the display.

def right_justify(text:str):

    print(" " * (70 - len(text)) + text)
# ----------------------------------------------------------------------------------------------------------------------------------
# Extra oef 2
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

    right_justify('monty')

if __name__ == "__main__":
    main()