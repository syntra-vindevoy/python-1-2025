# DIT NIET DOEN
# file = open("words.txt", "r") # Altijd sluiten zo snel mogelijk als je het niet meer nodig hebt.
#
# lines = file.readlines()
#
# file.close() # Altijd sluiten zo snel mogelijk als je het niet meer nodig hebt.
# Doe DIT.
# Methode 1
from urllib3.filepost import writer

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

#EXTRA from tp3_ch8 (read, write, and read/write as binary
#Writing
# with open("words.txt", "w") as file:
#     writer.write(line)
#     writer.close()

# with open("words.txt", "rb") as file:     #rb = Read as Binary
# with open("words.txt", "wb") as file:     #wb = Write as Binary