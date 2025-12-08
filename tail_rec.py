def fac(n):
    def helper(n, c):
        if n == 2:
            return c * n

        return n - 1, c * n

    if n == 0 or n == 1:
        return 1

    c = 1

    while n > 2:
        n, c = helper(n, c)

    return c * n

print(fac(5))