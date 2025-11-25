#V1) List first names (Met Yves als eerste) naam:classroom ; y=klinker
#V2) Remove all names starting with a vowel
#Wondelgem, turqua, zelzate, torhaut, gegaartsbergen, lede

classroom = ["Yves", "Brent", "Cristian", "Yves", "Femke", "Uwe"]

for name in classroom:
    if name[0] in "AEIOUY":
#         classroom.remove(name)    #De remove loopt over de lijst, nog eens, per keer de if true is
        delimiter = ' '
        s = delimiter.join(classroom)
        t = s.split(name).split(" ")
        t = t.split(" ")
        print(list(t))

# name for
#
# classroom.remove(name) if name[0].lower() in "aeiouy" for name in classroom:

#print(classroom)