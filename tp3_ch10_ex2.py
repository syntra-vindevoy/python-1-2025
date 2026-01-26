from datetime import datetime


def letter_count(word: str) -> dict:
    counts = {}

    for letter in word:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    return counts


def letter_count2(word: str) -> dict:
    return {letter:word.count(letter) for letter in word}


start = datetime.now()

t = 1000000
for _ in range(t):
    res = letter_count2("brontosaurus")

end = datetime.now()

print(end - start)
print(res)