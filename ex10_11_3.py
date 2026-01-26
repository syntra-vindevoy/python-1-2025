from pathlib import Path

words = Path("words.txt").read_text().splitlines()

longest = -1
longest_word = ""

for word in words:
    if len(word) < longest:
        continue

    if len(word) != len(set(word)):
        continue

    if len(word) > longest:
        longest = len(word)
        longest_word = word

print(longest_word, "has", longest, "letters")


longest = 0
longest_word = ""

for word in words:
    if len(word) < longest:
        continue

    letters = {}
    unique = True

    for letter in word:
        if letter in letters:
            unique = False
            break

        letters[letter] = 1

    if unique and len(word) > longest:
        longest = len(word)
        longest_word = word


print(longest_word, "has", longest, "letters")