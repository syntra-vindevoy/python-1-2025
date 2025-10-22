# DIT NIET DOEN
# file = open("words.txt", "r") # Altijd sluiten zo snel mogelijk als je het niet meer nodig hebt.
#
# lines = file.readlines()
#
# file.close() # Altijd sluiten zo snel mogelijk als je het niet meer nodig hebt.
# Doe DIT.
# Methode 1
with open("words.txt", "r") as file:
    lines = file.readlines()

for word in lines:
    print(word)

# Methode 2
with open("words.txt", "r") as file:
    while True:
        line = file.readline().strip()
        print(line)

        if not line:
            break