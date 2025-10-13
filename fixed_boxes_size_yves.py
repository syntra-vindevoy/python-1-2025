def print_single_line(corner: str, line: str, size, horizontal):
    for h in range(horizontal):
        print(corner,end=" ")

        for s in range(size):
            print(line,end=" ")
    print(corner, end="\n")

def print_edge_line(size: int, horizontal: int):
    print_single_line(corner="*", line="-", size=size, horizontal=horizontal)

def print_box_line(size: int, horizontal: int):
    print_single_line(corner="|", line=" ", size=size, horizontal=horizontal)

def draw_boxes(size: int, horizontal: int, vertical: int):
    for v in range(vertical):
        print_edge_line(size=size, horizontal=horizontal)

        for s in range(size):
            print_box_line(size=size, horizontal=horizontal)
    print_edge_line(size=size, horizontal=horizontal)

def main():
    draw_boxes(size=10, horizontal=5, vertical=5)

if __name__ == "__main__":
    main()