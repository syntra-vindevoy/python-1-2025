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
def main():
    triangle('L', 5)
    rectangle('H', 5, 4)
    bottle_verse(10)

if __name__ == "__main__":
    main()