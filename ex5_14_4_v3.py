""" This recurse function only works for positive integers of s, if n is negative the stop condition will not be attained and you will get a maximum recursion depth error"""
def recurse(n, s):
    if n == 0:
        print(s)
    else:
        recurse(n-1, n+s)

recurse(3, 0)