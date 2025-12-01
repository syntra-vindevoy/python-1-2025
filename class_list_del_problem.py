from datetime import datetime

times = 10000000

def with_remove():
    global provinces

    for p in provinces:
        if p[0] in "AEIOU":
            provinces.remove(p)

def with_pop():
    global provinces

    for i in range(len(provinces) - 1,0,-1):
        if provinces[i][0] in "AEIOU":
            provinces.pop(i)

def with_del():
    global provinces

    for i in range(len(provinces) - 1,0,-1):
        if provinces[i][0] in "AEIOU":
            del provinces[i]

def with_list_comp():
    global provinces

    _ = [p for p in provinces if p[0] not in "AEIOU"]

start = datetime.now()

for _ in range(times):
    provinces = ["Waals-Brabant", "Antwerpen", "Vlaams-Brabant",
                 "Luik", "Namen", "Henegouwen", "Luxemburg", "Limburg",
                 "West-Vlaanderen", "Oost-Vlaanderen"]

    with_remove()

end = datetime.now()

print(end - start)


start = datetime.now()

for _ in range(times):
    provinces = ["Waals-Brabant", "Antwerpen", "Vlaams-Brabant",
                 "Luik", "Namen", "Henegouwen", "Luxemburg", "Limburg",
                 "West-Vlaanderen", "Oost-Vlaanderen"]

    with_pop()

end = datetime.now()

print(end - start)


start = datetime.now()

for _ in range(times):
    provinces = ["Waals-Brabant", "Antwerpen", "Vlaams-Brabant",
                 "Luik", "Namen", "Henegouwen", "Luxemburg", "Limburg",
                 "West-Vlaanderen", "Oost-Vlaanderen"]

    with_del()

end = datetime.now()

print(end - start)


start = datetime.now()

for _ in range(times):
    provinces = ["Waals-Brabant", "Antwerpen", "Vlaams-Brabant",
                 "Luik", "Namen", "Henegouwen", "Luxemburg", "Limburg",
                 "West-Vlaanderen", "Oost-Vlaanderen"]

    with_list_comp()

end = datetime.now()

print(end - start)
