import math


def factorial(n):
    if n == 0:
        return 1

    result = n

    for i in range(2, n):
        result *= i

    return result


def factorial_recursive(n):
    if n == 0:
        return 1

    return n * factorial_recursive(n - 1)


import datetime

start_ts = datetime.datetime.now()

for i in range(100000):
    factorial_recursive(500)

end_ts = datetime.datetime.now()

print(end_ts - start_ts)

start_ts = datetime.datetime.now()

for i in range(100000):
    factorial(500)

end_ts = datetime.datetime.now()

print(end_ts - start_ts)


def rounded_pi(n):
    return round(math.pi, n)


def main():
    assert factorial(1) == 1, "factorial(1) must be 1"
    assert factorial(3) == 6, "factorial(3) must be 6"
    assert factorial(4) == 24, "factorial(4) must be 24"

    print(rounded_pi(5))

    x = factorial(5)
    print("De faculteit van 5 is", x)


if __name__ == "__main__":
    main()
