DEFAULT_NAME = "Syntra"


def say_hello(who: str = DEFAULT_NAME):
    name = "Vindevogel"

    print(f"Hello, {who}!")

    return name


def toto(l: list = None):
    if l is None:
        l = []

    print(f"Toto: {l}")
    return l


def main():
    global name
    name = "Yves"

    say_hello(name)

    print("name:", name)


if __name__ == "__main__":
    name = "Brent"

    main()
    print("name:", name)
