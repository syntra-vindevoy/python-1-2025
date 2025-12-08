def factorial(n):
    """How it's writen here, this function doesn't calculate factorial itself,
    but can be publicly used and still produce the accurate result."""
    if n == 0 or n == 1:  #Own check of the function.
        return 1

    def helper(n, c):
        """Used to handle calculations and data handeling, to then return it to its parent function."""
        if n == 1:  #Duplicate check, but is needed since n is called on line 12 with decrementing arguments.
            return c    #c is the variable used to temporarily store the current total result.

        return n - 1, c * n     #n is decreased by 1 per loop, and the multiplication is done to the number of c.
    c = 1   #0 * anything = 0   ;   1 * anything = anything ;   2(or more) is unreliable.
    while n > 2:
        # print("n:", n)
        # print("c:", c)
        n, c = helper(n, c) #Function returns a tuple(,) so you need a tuple to put it in.
        #n is declared in the factorial function, c hasn't so it's declared above as 1 as the neutral multiplication.

    return c

print(factorial(5))
print(factorial(1500))