def fac(n):
    if n == 0 or n == 1:
        return 1

    def helper(n, c):
        if n == 1:
            return c

        return n - 1, c * n

    c = 1

    while n > 2:
        n, c = helper(n, c)

    return c * n

print(fac(1500))