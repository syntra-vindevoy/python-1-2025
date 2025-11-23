def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)


def rounded_phi(n: int):
    import math

    rounded_phi = round(math.pi, n)
    return rounded_phi


def factorial(n):
    if n == 0:
        return 1
    result = n
    for i in range(2, n):
        result *= i
    return result


def main():
    assert factorial_recursive(3) == 6, "factorial(3) must be 6"
    assert factorial_recursive(4) == 24, "factorial(4) must be 24"
    assert factorial_recursive(5) == 120, "factorial(5) must be 120"
    x = factorial_recursive(5)
    print(x)
    print(rounded_phi(5))
    print(factorial(5))
    import datetime
    startds = datetime.datetime.now()
    for i in range(100000):
        factorial_recursive(500)
    endds = datetime.datetime.now()
    print(endds-startds)
    startds = datetime.datetime.now()
    for i in range(100000):
        factorial(500)
    endds = datetime.datetime.now()
    print(endds-startds)

if __name__ == "__main__":
    main()
