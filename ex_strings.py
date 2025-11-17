from tarfile import TruncatedHeaderError


def is_palindrome(word: str) -> bool:
    return word.lower() == word[::-1].lower()

def is_palindrome_alt(word: str) -> bool:
    word = word.lower()

    return  word == word[::-1]

def is_voodoo(word: str) -> bool:
    return is_palindrome(word[1:])

def is_voodoo_alt(word: str) -> bool:
    word = word.lower()

    moved = word[1:] + word[0]

    return word[::-1] == moved

assert is_voodoo("yves") == False

def is_anagram(word1: str, word2: str) -> bool:
    return sorted(word1.lower()) == sorted(word2.lower())

def is_in_words_alt(word: str) -> bool:
    with open("words.txt") as f:
        lines = f.readlines()

        for w in lines:
            if word == w.strip():
                return True

    return False

def is_in_words(word: str) -> bool:
    with open("words.txt") as f:
        words = f.read().split("\n")

        return word in words



def is_existing_anagram_alt(word1: str, word2: str) -> bool:
    if not(is_anagram(word1, word2)):
        return False

    return is_in_words(word1) and is_in_words(word2)


def is_existing_anagram(word1: str, word2: str) -> bool:
    if not(is_anagram(word1, word2)):
        return False

    with open("words.txt") as f:
        words = f.read().split("\n")

        return word1 in words and word2 in words


def is_existing_anagram(word1: str, word2: str) -> bool:
    if not(is_existing_anagram(word1, word2)):
        return False

    with open("words.txt") as f:
        words = f.read()
        words = f"\n{words}\n"

        return f"\n{word1}\n" in words and f"\n{word2}\n" in words

def is_real_anagram(word: str) -> bool:
    with open("words.txt") as f:
        words = f.read().split("\n")

        found = False
        anagram = False

        for w in words:
            if w == word:
                found = True
            elif is_anagram(w, word):
                anagram = True

            if anagram and found:
                return True

        return False




def most_vowels() -> str:
    with open("words.txt") as f:
        return sorted([{word:sum(1 for char in word if char in "aeiou")} for word in f.read().split("\n") if len(word) > 0], key=lambda d: list(d.values())[0])[-1]

print(most_vowels())

def longest_palindrome() -> str:
    length = -1
    longest = ""

    with open("words.txt") as f:
        words = f.read().split("\n")

        for w in words:
            if len(w) > length and is_palindrome(w):
                length = len(w)
                longest = w

    return longest
