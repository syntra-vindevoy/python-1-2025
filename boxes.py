def draw_boxes(size: int, horizontal: int, vertical: int):
    def print_single_line(corner: str, line: str):
        for h in range(horizontal):
            print(corner, end=" ")

            for s in range(size):
                print(line, end=" ")

        print(corner, end="\n")

    def print_edge_line():
        print_single_line(corner="+", line="-")

    def print_box_lines():
        print_single_line(corner="|", line=" ",)

    for v in range(vertical):
        print_edge_line()

        for s in range(size):
            print_box_lines()

    print_edge_line()


def main():
    draw_boxes(size=4, horizontal=5, vertical=3)


if __name__ == "__main__":
    main()
