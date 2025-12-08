def fac(n):
    if n == 0:
        return 1
    def helper(n, c):
        if n == 0:
            return c
        return n - 1, c*n
    c=1
    while n > 2:
        n, c = helper(n, c)
    return c*n


print(fac(1500)) #helper function countert de stack overflow - dus als je recursiviteit gebruikt







