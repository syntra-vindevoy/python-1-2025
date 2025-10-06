# Write a function called triangle that takes a string and an integer and draws a pyramid with the given height,
# made up using copies of the string. Here’s an example of a pyramid with 5 levels, using the string 'L'.

def triangle(brick:str = "=", length:int = 3):
    for i in range(length + 1):
        print(brick * i)

def main():
    triangle('L', 5)

if __name__ == "__main__":
    main()