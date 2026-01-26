l = ["yves", "niels"]
l = [None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
l = ["Yves", 1972]

l = []
l = list()

def toto():
    print("toto")

def tata():
    print("tata")

def india(lst: list):
    for l in lst:
        l()

india([toto, toto, tata, toto])

names = ["yves", "niels"]

# NEVER
for i in range(len(names)):
    print(names[i])

for name in names:
    print(name)

print(["toto", "tata", "titi"][0])
person = ["yves", 1972, ["Kruishoutem", "Wortegem-Petegem", "Zingem", "Oudenaarde", "Gentbrugge"]]

cities = person[2]
print(person[0], "was born in", person[2][0])


print((list("yves")))

first = names[0]
last = names[-1]

print(first, last)

names = ["yves", "niels"]
names[0] = "jacques"

print(names)

if "yves" in names:
    pass

print(list(range(0,4)))

print(min(names))

t1 = ["yves", "niels"]
t2 = ["marleen", "katya"]

from datetime import datetime

start = datetime.now()

for i in range(1000000):
    t3 = t1 + t2

end = datetime.now()
print(end - start)

start = datetime.now()

for i in range(1000000):
    t1.extend(t2)

end = datetime.now()

names = ["yves", "niels"]

print(end - start)

print(names.pop(0))

names.remove("niels")
print(names)

names = ["yves", "niels"]

del names[1:]


names = sorted(names)

names.sort()

print(names)


def toto(names : list[str] = None):
    if names is None:
        names = []

    names = names or []