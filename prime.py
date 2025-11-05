def is_prime(n):
    assert type(n) == int
    assert n > 0

    if n == 1 or n % 2 == 0:
        return False

    #for i in range(3, int(math.sqrt(n)) + 1, 2):
    for i in range(3, n ** 0.5 + 1, 2):
        if n % i == 0:
            return False
    return True