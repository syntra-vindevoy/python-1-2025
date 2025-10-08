def repeated_call(func, number, *args, **kwargs):
    for i in range(number):
        func(*args, **kwargs)

def hello_world(name: str):
    print(f"Hello {name}!")

def main():
    repeated_call(hello_world, 3, name="Yves")

if __name__ == "__main__":
    main()
