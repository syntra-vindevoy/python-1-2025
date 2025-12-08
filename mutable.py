a = "yves"
b = a

print(a)
print(b)

a = "niels"

print(a)
print(b)

c = 1
d = 2
print(c)
print(d)

c= 3
print(c)
print(d)

l1 = [1, 2, 3]
l2 = l1
print(l1)
print(l2)

l1.append(4)
print(l1)
print(l2)

l2 = l1.copy()
l1.append(5)
print(l1)
print(l2)

def change_str(s: str):
    s = s.lower()

a = "Yves"
change_str(a)
print(a)

def change_list(lst: list):
    lst.copy().append(4)

l = [1, 2, 3]
change_list(l)
print(l)

l = []

def my_function(lst: list = []):  # BAD !
    lst.append(4)

my_function(l)
print(l)

def my_function(lst: list = None):
    if lst is None:
        lst = []
