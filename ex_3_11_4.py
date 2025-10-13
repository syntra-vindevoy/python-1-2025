def rectangle(*,letter:str="H",width:int=5,height:int=4):
    assert type(letter)==str, "letter must be a string"
    assert type(width)==int, "width must be a integer"
    assert type(height)==int, "height must be a integer"
    for i in range(height):
        print(width*letter)

def main():
    rectangle(letter="H",width=5, height=4)

if __name__ == "__main__":
    main()