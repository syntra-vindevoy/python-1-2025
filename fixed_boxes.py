def print_line(corner: str, line: str):
    for i in range(2):
        print(corner, end=" ")
        print(f"{line} " * 4, end="")

    print(corner)

def print_edge_line():
    print_line(corner="+", line="-")

def print_box_line():
    for j in range(4):
        print_line(corner="|", line=" ")


def draw_boxes():
    print_edge_line()

    for i in range(2):
        print_box_line()
        print_edge_line()


def main():
    draw_boxes()

if __name__ == '__main__':
    main()
