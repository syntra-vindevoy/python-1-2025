def triangle(char: str, size: int):                     # Dit is geen "one-liner"
    for i in range(size):
        print(char * (i+1))

triangle(char="*", size=5)

print( "\n".join(["*" * (i + 1) for i in range(5)]))    # Dit is wél een "one-liner"