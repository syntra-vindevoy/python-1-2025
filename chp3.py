max_char = 40
char = '#'

#Versie Brent
def line_with_stars(text):
    padding = (max_char - len(text)) // 2
    return f"{char * (padding - 1)} {text} {char * padding}"

#Versie Yves
def starred_name(last_name, first_name):
    name = last_name + ' ' + first_name
    postfix = (max_char - 2 - len (name)) // 2
    prefix = (max_char - 2 - len (name)) - postfix
    print("*" * prefix, name, "*" * postfix)

#print resulaten
print(line_with_stars("Yves"))
print(line_with_stars("Brent"))
print(line_with_stars(""))
print(char * max_char + "\n")
starred_name("Vindevogel", "Yves")
starred_name("Hendricx", "Brent")