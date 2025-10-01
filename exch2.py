import math

radius = 5
volume = (4 / 3) * math.pi * math.pow(radius, 3)
print("circle with radius", radius, "cm, creates a sphere with volume ", volume, "cm³")
volume_rounded = round(volume, 0)
alternative_vol = round(((4 / 3) * 3.1415 * 5 * 5 * 5), 0)
assert volume_rounded == alternative_vol

var1 = 42
check = math.pow(math.cos(var1), 2) + math.pow(math.sin(var1), 2)
print(check)
assert check == 1

e1 = math.e**2
e2 = math.pow(math.e, 2)
e3 = math.exp(2)
print(e1, e2, e3)
e1 = round(e1, 2)
e2 = round(e2, 2)
e3 = round(e3, 2)
assert e1 == e2
assert e1 == e3

# math.log10() hiermee kan je de lengte van een getal bereken print(int(math.log0(a)+1)
