from pyflakes.checker import counter
import re


def palindrome(word:str)->bool:
    return word.lower() == word[::-1].lower()

def voodoo(word:str)->bool:
    return palindrome(word[1:])

def anagram(word1:str, word2:str)->bool:
    if len(word1) != len(word2):
        return False
    word1 = word1.lower()
    word2 = word2.lower()
    for letter in word1:
        if letter in word2:
            word2 = word2.replace(letter, "")

    return word2 == ""

def anagram_sorted(word1:str, word2:str)->bool:
    return sorted(word1.lower()) == sorted(word2.lower()) #dit is een betere methode

def check_anagram(word:str):
    with open("words.txt") as f:
        lines = f.readlines()
        for w in lines:
            if word==w.strip():
                return True
    return False

def is_in_words(word:str)->bool: #betere functie geschreven door Yves
    with open("words.txt") as f:
        words = f.read().split("\n")
        return word in words

def is_valid_anagram(word1:str, word2:str)->bool:
    if anagram_sorted(word1, word2):
        return check_anagram(word1) and check_anagram(word2)
    return False

def is_existing_anagram(word1:str, word2:str)->bool:
    if not(anagram_sorted(word1, word2)):
        return False

    with open("words.txt") as f:
        words = f.read().split("\n")
        return word1 in words and word2 in words

def is_existing_anagram2(word1:str, word2:str)->bool:
    if not(anagram_sorted(word1, word2)):
        return False

    with open("words.txt") as f:
        words = f.read()
        words = f"\n{words}\n"
        return f"\n{word1}\n" in words and f"\n{word2}\n" in words

def longest_palindrome_robin():
    with open("words.txt") as f:
        lines = f.readlines()
        longest = -1
        longest_palindrome = []
        for w in lines:
            s = w.strip()
            if palindrome(s):
                length = len(s)
                if length > longest:
                    longest = length
                    longest_palindrome = [s]
                elif length == longest:
                    longest_palindrome.append(s)

        return longest_palindrome

def longest_palindrome_yves():
    length = -1
    longest = ""
    with open("words.txt") as f:
        words = f.read().split("\n")

        for w in words:
            if len(w) > length and palindrome(w):
                length = len(w)
                longest = w
    return longest

def head_with(file_to_read, num_lines, file_to_write=None):
    with open(file_to_read, 'r') as f:
        lines = []
        counter = 0
        while counter < num_lines:
            line = f.readline()
            if line == '':
                break  # End of file
            lines.append(line)
            counter += 1

    if file_to_write is not None:
        with open(file_to_write, 'w') as out:
            for line in lines:
                out.write(line)
    else:
        for line in lines:
            print(line, end='')  # lines already contain \n



def head(file_to_read, num_lines, file_to_write=None):

    f = open(file_to_read, 'r')
    lines = []

    counter = 0
    while counter < num_lines:
        line = f.readline()
        if line == '':
            break  # End of file
        lines.append(line)
        counter += 1

    f.close()

    if file_to_write is not None:
        out = open(file_to_write, 'w')
        for line in lines:
            out.write(line)
        out.close()
    else:
        for line in lines:
            print(line, end='')  # lines already contain \n

def uses_any(word, letters):
    """Return True if the word uses any of the letters."""
    for letter in letters:
        if letter in word:
            return True
    return False

def wordle(word):
    assert len(word.strip()) == 5, "word should be five letters long"
    target = "mower"
    word = word.lower()
    forbidden_letters = 'spadclrkt'
    if word[4] is not 'm':
        return False
    if 'e' not in word:
        return False
    if word[2] == "e" or word[3]=="e" or word[4] == "e" or uses_any(word, forbidden_letters):
        return False
    return True

def find_words():
    with open("words.txt") as f:
        lines = f.readlines()
        words = []
        for w in lines:
            wordcheck = w.strip()
            if len(wordcheck) == 5:
                if wordle(wordcheck)==True:
                    words.append(wordcheck)
    return words

def montechristo():
    # Regex pattern
    pattern = r'\b(pale|pales|paled|paleness|pallor)\b'
    counter = 0
    with open("montechristo.txt","r",encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            line = line.lower()
            if re.search(pattern, line):
                counter += 1
    return counter

def any_lowercase1(s):
    """ this will not work the loop will stop after the first letter, if it is upper case the function returns False"""
    for c in s:
        if c.islower():
            return True
        else:
            return False

def any_lowercase2(s):
    """ this doesn't check the input but a string c which will always return true"""
    for c in s:
        if 'c'.islower():
            return 'True'
        else:
            return 'False'

def any_lowercase3(s):
    """only last number is returned because you reassign during your loop"""
    for c in s:
        flag = c.islower()
    return flag

def any_lowercase4(s):
    """ yes this will work, flag starts as False, if c.islower() is False then flag stays False, if it is True it will become True because the or statement, True will always stay true"""
    flag = False
    for c in s:
        flag = flag or c.islower()
    return flag

def any_lowercase5(s):
    """ if we encounter one letter that isn't lowercase then we return false and get kicked out, so this doesn't work as intended"""
    for c in s:
        if not c.islower():
            return False
    return True

def rotate_letter(letter,n):
    letter = letter.lower()
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    position = alphabet.index(letter)
    position = (position + n) % len(alphabet)
    return alphabet[position]

def rotate_word(word,n):
    rotated_word = ""
    for letter in word:
        rotated_word += rotate_letter(letter,n)
    return rotated_word

def rotate_sentence(sentence,n):
    rotated_sentence = ""
    for letter in sentence:
        if letter.isalpha():
            rotated_sentence += rotate_word(letter,n)
        else:
            rotated_sentence += letter
    return rotated_sentence


""" zoek woord met meeste klinkers"""

def main():
    print(palindrome('Radar'))
    print(voodoo('voodoo'))
    print(anagram("listen", "silent"))
    print(anagram("evil","vile"))
    print(check_anagram("vile"))
    print(longest_palindrome_robin())
    # Example usage:
    #head_with('example.txt', 5)  # Display first 5 lines
    #head_with('example.txt', 3, 'output.txt')  # Write first 3 lines to output.txt
    head('example.txt', 5)
    head('example.txt', 4, 'output.txt')
    print(wordle('mover'))
    print(find_words())
    print(montechristo())
    print("banana".count('a'))
    print(any_lowercase2('banana'))
    print(rotate_word("cheer",7))
    print("What do you call a song sung in an automobile?"+ rotate_sentence("N pnegbba",13)+",")
    print("What to you call a deer with no eyes?"+rotate_sentence("Ab rlr qrre",13)+".")
    print(rotate_sentence("Uv gurer. Guvf vf abg ernyyl wbxr. Whfg univat fbzr sha jvgu gubfr jub pna'g ebg13 na negvpyr. Gb or ernyyl zrna, sbyybj-hc gb guvf negvpyr jvgu fbzrguvat yvxr Obl, gung jnf gur shaavrfg wbxr V rire urneq! Stush",13))
    assert anagram("staarb", "raatsc")== False

if __name__ == '__main__':
    main()

