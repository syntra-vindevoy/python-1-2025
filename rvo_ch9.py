""" maak een lijst van alle voornamen van de mensen die hier zitten en je neemt van iedere persoon de voornaam"""
classroom = ["yves","femke","cristian","brent","jeroen","robin","uwe","bas","hendrik-jan"]

def del_with_vowels(lst:list)->list:
    vowels = ["a","e","i","o","u", "y"]
    for l in lst[:]:
        if l[0] in vowels:
            lst.remove(l)
    return lst

provinces = ["west-vlaanderen","oost-vlaanderen","antwerpen","limburg","vlaams-brabant","waals-brabant","henegouwen","luik","namen","luxembourg"]

def del_with_consonants(lst:list)->list:
    vowels = ["a", "e", "i", "o", "u"]
    for p in lst[:]:
        if p[0] in vowels:
            continue
        else:
            lst.remove(p)
    return lst

print(provinces)
print(del_with_vowels(classroom))
print(del_with_consonants(provinces))
