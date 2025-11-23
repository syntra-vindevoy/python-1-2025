a = 2
b = 3

c = a
a = b
b = c
print(a)
print(b)
assert a == 3
assert b == 2
# methode1

a = 2
b = 3
a = a ^ b
print(a)
b = b ^ a
print(b)
a = a ^ b
print(a)
assert a == 3
assert b == 2
# methode2 xor chatgpt - waarschijnlijk de snelste - als je dit doet, moet je commentaar bijschrijven

a = 2
b = 3
a = a + b
print(a)
b = a - b
print(b)
a = a - b
print(a)
assert a == 3
assert b == 2
##methode3

a, b = (
    b,
    a,
)  # werkt ook in python - wat gebeurt hierachter? Python gaat eerst de rechterkant doen, dat is een tuple dus is eigenlijk (b,a), hij gaat dat ergens saven. Dan kent hij dat toe als een kant, of één veriable of exact hetzelfde aantal element, dan pakt hij eerste element en steekt dat in eerste variabele, pakt tweede element steekt dat in de tweede variabele.
