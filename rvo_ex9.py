def is_anagram(word1: str, word2: str) -> bool:
    word1 = word1.lower()
    word2 = word2.lower()
    return sorted(word1) == sorted(word2)

def find_anagrams(word1: str) -> list:
    anagrams = []
    word1 = word1.lower()
    with open("words.txt") as f:
        for line in f:
            line = line.strip()
            word2 = line.lower()
            if is_anagram(word1, word2):
                anagrams.append(line)
    return anagrams

def reverse_word(word):
    return "".join(reversed(word))

def is_palindrome(word):
    return word == reverse_word(word)

def find_palindromes(length: int) -> list:
    palindromes = []
    with open("words.txt") as f:
        for line in f:
            line = line.strip()
            word = line.lower()
            if is_palindrome(word) and len(word) == length:
                palindromes.append(word)
    return palindromes

def reverse_sentece(sentence: str) -> str:
    words = sentence.split(sep=" ")
    words = [w.lower() for w in words]
    words = words[::-1] #je kan ook words = words.reverse() gebruiken
    words[0] = words[0].capitalize()
    return " ".join(words)

def reverse_sentence_oneline(sentence: str) -> str:
    return (" ".join(sentence.split(sep=" ")[::-1])).capitalize()

def total_length(): #je kan ook gewoon content = f.read, dan content.split("\n") dan joinen en return, gewoon een counter kan ook, je kan ook ineens \n replacen met lege space, je zou ook op basis van ascii u CRLF uit kunnen smijten
    full_list = []
    with open("words.txt") as f:
        for line in f:
            line = line.strip()
            full_list.append(line)
    full_list = "".join(full_list)
    return len(full_list)


def main():
    anagrams = find_anagrams("takes")
    print(anagrams)
    print(find_palindromes(7))
    print(reverse_sentece("Reverse this sentence"))
    print(reverse_sentence_oneline("Reverse this sentence"))
    print(total_length())


if __name__ == '__main__':
    main()