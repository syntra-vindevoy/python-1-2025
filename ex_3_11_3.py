def triangle(*,character:str ='l', height:int =5):
    assert type(character) == str, "character is not str"
    assert type(height) == int, "height is not int"
    for i in range(height):
        print(i*1*character)


def main():
    triangle(character='x',height=8)

if __name__ == "__main__":
    main()

