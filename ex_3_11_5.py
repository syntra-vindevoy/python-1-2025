def bottle_reverse(*,length: int = 99):
    assert type(length) == int, 'length is not an integer'

    def bottle_verse(*, length: int = 99):
        return print(str(length) + " bottles of beer on the wall\n" + str(
            length) + " bottles of beer\nTake one down, pass it around")

    for i in range(length,0,-1):
        bottle_verse(length=i)

def main():
    bottle_reverse()

if __name__ == "__main__":
    main()
