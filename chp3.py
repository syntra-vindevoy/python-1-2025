# #Versie Brent
# def line_with_stars(text):
#     padding = (max_char - len(text)) // 2
#     return f"{char * (padding - 1)} {text} {char * padding}"
#Kan ik, zonder een if statement te gebruiken, ervoor zorgen dat
# als de text variabe leeg is, geen spatie toont?
# -Stel, je doet spaties = round(1 / len(text)). en dan " " * spaties.

#Versie Yves
#   Position parameters kunnen worden gevuld zonder hun variabele naam ervor te zetten. Dit is niet altijd consistent en kan tot problemen zorgeb.
#   Je kan een waarde per ongelijk in een verkeerde parameter zetten, zonder het te weten. Met een naam ervoor gebeurt dat niet.
#               (*....      alle parameters NA het sterretje kunnen niet meer positioneel aangesproken worden
def starred_name(*last_name: str, first_name, total_width = 60, char = "*"):
    #                        : str     door dit na een parameter te zetten, HINT je dat enkel een waarde geacepteerd wordt van dat specifieke type. (het runt, maar kan chrachen door logica "symantic error)
    #                                              total_width = 60        Door " = waarde" na een parameter te zetten geef je het een default waarde zodat een oproep van de methode die niet moet vermelden.
    #                                              total_width: int = 60        Je zet type verwachting vóór de default waarde
    assert type(last_name) is str, "Last name must be a string"
    name = last_name + f" {char} " + first_name
    postfix = (total_width - 2 - len (name)) // 2
    prefix = (total_width - 2 - len (name)) - postfix

    print(char * prefix, name, char * postfix)

#print resulaten
# print("\n* Brent " + "*" * 40)
# print(line_with_stars("Yves"))
# print(line_with_stars("Brent"))
# print(line_with_stars(""))
print("\n-Yves " + "*" * 34) #40 tekens
starred_name("Vindevogel", "Yves", 40)
starred_name("Hendricx", "Brent", 40, "#")
starred_name("Marginet", "Christian", char = "=")
starred_name(total_width = 30, last_name="Van Acker", char = "!", first_name = "Femke")
print("*" * 40)