# import sys
# import debug
# sys.exit(0)

#Benamingen die mogen, maar niet in formele code
me = "Brent Hendricx"
you = 'Yves Vindevogel'

#Benamingen liever nooit gebruiken
een = 1 #Naam mogelijk, niet aangeraden
tweeeneenhalf = 2.5 #Decimal point als punt
toto = 2,5 #Decimal point als komma

print("hello", "world", me, sep="-", end="")

#types van waardes in variabelen
print(type(me)) #Bij run = Geeft <class 'str'>
print(type(you))  #Bij run = Geeft <class 'str'>
print(type(een))  #Bij run = Geeft <class 'int'>
print(type(tweeeneenhalf)) #Bij run = Geeft <class 'float'>

#ChatGPT geeft dit als antwoord om de antwoorden hierboven te krijgen
print(isinstance(me, str))
print(isinstance(een, int))
#Verschil bij type en isinstance: type is in het algemeen gebruikbaar voor het opvragen van het type van een variabel (Maurice is een kat, is geen beest)
#                                 isinstance let op het overerven als je vraagt of "Maurice" een type beest is. (Maurice is een kat, is een beest)


#Getallen en type
a = 1       #int
b = 2       #int
c = a + b   #int
d = 2.5     #float
e = c + d   #float
print(e)
print(type(e))

print(2 + 2.0) #type is 4.0 en dus een float

print(1 - 2)    #int
print(2 * 7)    #int
print(4 ** 2)   #int Math.Pow(4,2), Macht tot de 2de
print(4 / 2)    #geeft altijd een float omdat het "delen" is. Geen "if" om te checken, het moet gwn snel gaan.
print(2 / 3)    #oneindige getallen achter decimal is 16 na de komma
print(4 // 3)   #resultaat 1
print(-4 // 3)  #resultaat -2
print(7 % 2)    #resultaat 1        modulo = geeft de rest van een deling

print(7 ^ 2)    #binaire rekensom (5)
print(6 ^ 3)    #binaire rekensom (2)
print(6 >> 2)   #binaire rekensom (1)
print(6 >> 1)   #binaire rekensom (3)

#lang binair nummer snel omrekenen (enkel bij positieve gehele getallen)
# 110110110 = 438
# startend bij het eerste 1-tje (volgende binair is 1? doe maal 2 plus 1) (volgende binair is 0, doe maal 2)
# 1 1
# 1 (* 2 + 1)   3
# 0 (* 2)       6
# 1 (* 2 + 1)   13
# 1 (* 2 + 1)   27
# 0 (* 2)       54
# 1 (* 2 + 1)   109
# 1 (* 2 + 1)   219
# 0 (* 2)   438

file = "C:\\Users\\Brent\\Desktop\\Python\\Syntra\\hello.py"
#Een \ in text is voor het volgende speciale teken gewoon te maken (schrijft de \ dan ook niet)

a = 1
a = "Yves"
b = "Toto"

# a=1
# print(a) #1
a="Brent"
print(a) #Brent
b="Hendricx"
print(a+b) #Brent Hendricx
#print(a-b) #ERROR, strings kunnen niet bij afgetrokken worden
print(" "*30) #30 spaties
print("              ") #NOOIT zo doen

x=1
y="test"
#print(x+y) #Geeft fout, int en string kunnen niet bij elkaar worden getelt

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

print(len("Yves"))  #len = Length van de string (met spaties), resultaat = 5

# Naam voor versies v#(1).#(2).#(3) bv. v2.14.3
# (1) Veranderen in "version breaking updates" (nieuwe functies die oude functies breken)
# (2) Veranderen in "functionality updates" (nieuwe functionaliteiten zonder code te breken)
# (3) Veranderen in "bugfixes" (code aanpassen dat niet breekt zoals een foutje corrigeren)