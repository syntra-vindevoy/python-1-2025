#oefeningen Extra (Wissel a en b van waarden)
a = 2
b = 3

#CODE HERE (vers 1)
c = b
b = a
a = c

#assert
assert a == 3
assert b == 2
a = 2
b = 3

#CODE HERE (vers 2)
a = a + b #6
b = a - b #2
a = a - b #3

#assert
assert a == 3
assert b == 2
a = 2
b = 3

#CODE HERE (vers 3)
a = a ^ b
b = a ^ b
a = a ^ b

#assert
assert a == 3
assert b == 2
a = 2
b = 3

#CODE HERE (vers 4)
a, b = b, a

#assert
assert a == 3
assert b == 2