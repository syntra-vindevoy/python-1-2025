def say_hello():
    print("Hello, world!")


def do_twice(f):
    f()
    f()


do_twice(say_hello)
