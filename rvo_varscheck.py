def hello_world(name):
    print(f"hello {name}")


def repeated_call(func, number, *args, **kwargs):
    for i in range(number):
        func(*args, **kwargs)


def main():
    text = "world"
    repeated_call(hello_world, 4, text )


if __name__ == "__main__":
    main()
