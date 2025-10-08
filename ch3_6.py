def delen(x: float, y: float) -> float:
    return x / y


def main():
    y = 0
    x = 4
    z = delen(x, y)


if __name__ == "__main__":
    assert delen(5, 1) == 5

    failure = False

    try:
        delen(5, 0)
    except ZeroDivisionError:
        failure = True

    assert failure, "This should have raised ZeroDivisionError"
