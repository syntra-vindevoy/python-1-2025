def factorial(n):
    assert n > 0, "n must be greater than 0"

    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


try:
    print(factorial(-1))
except Exception as e:
    print("Error occurred: " + str(e))
