def print_right(*,input: str, width: int=40):
    assert type(input) == str, "input must be a string"
    assert type(width) == int, "width must be an integer"
    if len(input) > width:
        return print("input is larger than width")
    length_input = len(input)
    rest_width = width - length_input
    print(rest_width*" ",input,sep="")

def main():
    print_right(input="hello")
    print_right(input="hello world")
    print_right(input="hello world testing")

if __name__ == "__main__":
    main()
