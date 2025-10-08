def rectangle(char: str, hor: int, ver: int):
    for i in range(ver):
        print(char * hor)

rectangle(char="*", hor=4, ver=3)


def void_func():
    a = 1
    b = 2
    c = a + b


print(void_func())