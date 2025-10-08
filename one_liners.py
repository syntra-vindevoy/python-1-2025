def triangle(char: str, size: int):
    for i in range(size):
        print(char * (i + 1))

triangle(char="*", size=5)

# print( "\n".join(["*" * (i + 1) for i in range(5)]))


def oneline_grid(box_width, amount_width, box_height, amount_height):
    print((((" ".join(" " for i in range(box_width + 1))).join(
        "|" for i in range(amount_width + 1)) + "\n") * box_height).join(
        (("-".join(" " for i in range(box_width + 1))).join("+" for i in range(amount_width + 1)) + "\n") for i in
        range(amount_height + 1)))

oneline_grid(box_width=4, amount_width=5, box_height=5, amount_height=2)