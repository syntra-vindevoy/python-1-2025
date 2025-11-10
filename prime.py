import math


def is_prime(n):
    """
    
    :param n:
    :return:
    """
    assert type(n) is int
    assert n > 0

    if n == 1:
        return False

    if n % 2 == 0:
        return False

    for i in range(3, n ** 0.5 + 1, 2):
        if n % i == 0:
            return False

    return True