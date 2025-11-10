def uses_any(word, letters):
    for letter in word():
        if letter in letters:
            return True

    return False

def uses_none(word, letters):
    for letter in letters:
        if letter in word:
            return False

    return True

def uses_only(word, letters):
    for w in word:
        if w not in letters:
            return False

    return True

def uses_all(word, letters):
    for letter in letters:
        if letter not in word:
            return False

    return True

def check_word(word, letters, required = None):
    if required is not None:
        assert required in letters, "required must be in letters"

    if len(word) < 4:
        return False


    if required is not None and required not in word:
        return False

    return uses_any(word, letters)

def word_score(word: str, letters: str):
    for w in word:
        if w not in letters:
            return 0

    extra_points = 7

    for letter in letters:
        if letter not in word:
            extra_points = 0
            break

    if len(word) == 4:
        return 1
    else:
        return len(word) + extra_points


def uses_all(word, letters):
    return uses_only(letters, word)

print(word_score("card", "acdlort"))
print(word_score("color", "acdlort"))
print(word_score("cartload", "acdlort"))