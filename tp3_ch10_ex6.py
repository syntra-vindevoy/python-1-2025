from pathlib import Path

words = Path("words.txt").read_text().splitlines()
valid_words = {word: True for word in words if len(word) > 3}

# valid_words = {}
# for word in words:
#    valid_words[word] = True

def is_interlocking(word):
    part1 = word[0::2]
    part2 = word[1::2]

    return part1 in valid_words and part2 in valid_words, word, part1, part2

for word in words:
    if len(word) < 8:
        continue

    interlocks, word, part1, part2 = is_interlocking(word)

    if interlocks:
        print(word, part1, part2)