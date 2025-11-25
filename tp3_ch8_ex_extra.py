#Oefening 1: Is een woord een palindroom (een woord dat omgekeerd hetzelfde woord is)
def is_palindrome(word:str):
    return word.lower() == word[::-1].lower()
    #                      word [starts at None(=first character): ends at None(=last character): step amount is -1(step backwards 1 step)
    #                                                  -1 loops to the back, then -1 each time, then stops returning if character is None

#Oefening 2: Is een woord een voodoo woord (de eerste letter van het woord verplaatst naar vanachter is dan gelijk aan het woord omgekeerd)
def is_voodoo(word:str):
    return word.lower()[1:] + word.lower()[0] == word[::-1].lower()
    #       start word at position 1(second character since pos 0, is first character) then adds character 0 of word (first character)
    #       compares to reverse word with [::-1](use for backwards word)

def is_voodoo_alt(word:str): #Methode-in-methode case
    return is_palindrome(word[1:0])
    #   If the word should be a palindrome, the first letter shouldn't be considered.
    #   Then we can use is_palindrome to check the word without the first letter if the word without the first letter is the same backwards.

#Oefening 3: Is een woord een anagram (een ander woord vormend met de letters van het originele woord) (nieuw woord moet niet bestaan)
def is_anagram(word1:str, word2:str):
    return sorted(word1.lower()) == sorted(word2.lower())
    #   Searching for words in words.txt is niet optimal. When you sort a word, the characters are sorted by order in the ASCII-table.
    #   IF the two words share the same (amount of characters AND) the same letters, the sorted letters should be ordered the same,
    #   and should be the same. So a compare between the two sorted words is enough.

#Oefening 4: Is het nieuw gevormd woord in oef3 een bestaand woord in words.txt
def is_anagram_word(word1:str, word2:str):
    if not is_anagram(word1, word2): return False #First check if it's an anagram. If already false, uses less performance then checking a whole word list first.
    with open("words.txt") as file:
        words = file.read()
        words = f"\n{words}\n"

        return f"\n{word1}\n" in words and f"\n{word2}\n" in words

def is_anagram_word_alt(word1:str, word2:str): #TO EDIT
    if not is_anagram(word1, word2): return False
    with open("words.txt") as file:
        words = file.read().strip("\n")
    return False
    #return word in words

def is_anagram_word2(word:str): #Checking if anagram with only 1 varia & most optimal with only reading words.txt once.
    with open("words.txt") as file:
        words = file.read().strip("\n")

        found = False
        anagram = False

        for w in words:
            #First new_word is either the word or an anagram or irrelevant, so if the word is found, we don't check for if it is it's own anagram.
            #If new_word is not the word, it's either an anagram or irrelevant. Irrelevant does nothing and goes to next word in this methode.
            #Only when 2 words are found, one the word and the other it's anagram, returns the method true (does not need to go through the whole list of words)
            if w == word:
                found = True
            elif is_anagram_word(w, word):
                anagram = True
            if anagram & found:
                return True
        return False

#Oefening 5: Wat is het langste palindroom in words.txt
def longest_palindrome_word(word:str):
    with open("words.txt", "r") as file:
        words = file.read().strip("\n") #Best way to get only words without a newline attached. "Readline()" doesn't remove the \n.

    loong = ""
    length_loong = -1   #Uses int instead of len() to not keep calculating len() each time. -1 to give "lowest" value that needs to be overridden with the longest length
    for word in words:
        if len(word) > length_loong and is_palindrome(word):
            loong = word
            length_loong = len(word)
    return loong

# def word_most_vowels(): #One-liner challenge
#     with open("words.txt") as file: words = file.read().strip("\n")
#         return [i**2 for i in range(10) if i % 2 == 0]

def main():
    assert is_palindrome("keek") == True
    assert is_voodoo("voodoo") == True
    assert is_anagram("staar", "tsaar") == True
    assert is_anagram_word("staar", "raast") == True

if __name__ == "__main__":
    main()