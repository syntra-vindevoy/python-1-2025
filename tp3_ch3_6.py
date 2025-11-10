def delen(x: float, y: float) -> float:
    return x / y

def main():
    print(delen(4, 0)) # Runtime error door met 0 te delen.

if __name__ == "__main__":
    assert delen(5, 1) == 5

    failure = False

    try:
        delen(5, 0)
    except ZeroDivisionError:
        failure = True

    assert failure == True
    main()