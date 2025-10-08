a = 2
b = 3

# c = b
# b = a
# a = c

# a = a + b
# b = a - b
# a = a - b


# a = a ^ b
# b = b ^ a
# a = a ^ b

a, b = b, a

assert a == 3
assert b == 2
