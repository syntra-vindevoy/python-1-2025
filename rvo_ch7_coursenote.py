""" das hier slechte code
file = open("words.txt","r") #r = read

lines = file.readlines()

file.close() #file geopend dus je moet hem sluiten ook, soms ga je vastlopen op lijn 3 -- dus niemand kan aan die file
"""
with open("words.txt","r") as file:
    lines = file.readlines()
    #nadeel het zit in geheugen, voordeel zit in geheugen. Nog voordeel, uw file is direct weer vrijgegeven. Afwegen, memory vs efficiency
    #zodra with gedaan is, wordt de file gesloten -> dit is een context manager, een deel code die je mogelijks vergeet zo schrijven zodat je dit. Geen file close.
for word in lines:
    print(word.strip()) #backslash n /n staat er nog , dus we krijgen lege lijntjes


"""methode 2: gaat lopen wanneer er een line is om te lezen, tot alle lijntjes gelezen zijn, nadeel is uw file staat open"""

with open("words.txt","r") as file:
    while True:
        line = file.readline().strip()
        print(line)

        if not line:
            break

""" methode 3 - nadeel hier is dat het weer nog op staat"""
for line in open("words.txt","r"):
    print(line)
