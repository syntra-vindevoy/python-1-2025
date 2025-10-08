import sys

import debug

sys.exit(0)

print("hello", "world", sep="-", end="")

me = "Yves Vindevogel"
you = "Brecht"


print(type(me))

a = 1
b = 2
c = a + b
d = 2.5
e = c + d
print(e)
print(type(e))

print(2 + 2.0)

print(1 - 2)
print(2 * 7)
print(2 / 3)
print(-4 // 3)
print(7 % 2)

print(7 ^ 2)
print(6 ^ 3)
print(6 >> 2)
print(6 >> 1)

a = 1
a = "Yves"
b = "Toto"

print(a + b)
print("ud" * 30)


punten = 90
totaal = 100
result = punten / totaal * 100
print("U behaalde " + str(result) + " punten")
print("U behaalde", result, "punten")
print(f"U behaalde {result} punten")

s = """
sqfs
fdsqf
dsqfdsq
fds
q
"""

#
# i = input("Geef een getal:")
# print("U behaalde" + str(int(i)  / 100) + "percent")

print(len("Yves"))
