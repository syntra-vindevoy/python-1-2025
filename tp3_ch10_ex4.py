from tp3_ch10_ex2 import letter_count

def find_repeats(word: str) -> dict:
    letters = letter_count(word)

    return {letter:letters[letter] for letter in letters if letters[letter]>1 }

def find_repeats_alt(letters: dict) -> dict[str, int]:
    return {letter:value for letter, value in letters.items() if value > 1}

def find_repeats_2(word: str) -> dict:
    counts = {}
    for letter in word:
        if letter in counts:
            counts[letter] += 1
        else:
            counts[letter] = 1

    repeats = {}
    for letter, count in counts.items():
        if count > 1:
            repeats[letter] = count

    return repeats

print(find_repeats('brontosaurus'))