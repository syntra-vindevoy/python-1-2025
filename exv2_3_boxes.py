def box(*,size: int = 6, length:int = 4, width:int = 4):
    assert type(length) == int and type(width) == int and type(size) == int
    dashes_width = size - 2
    first_line = "+ " + dashes_width * "- "
    others = "| " + dashes_width * "  "
    for k in range(length):
        print(first_line*width+"*")
        for i in range(dashes_width):
            print(others*width+"|")
    print(first_line*width+"*")

def main():
    box(size=4,length=3,width=2)

if __name__ == "__main__":
    main()

