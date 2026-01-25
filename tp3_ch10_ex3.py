def get_unique_letter_words(bigger_then: str):
    words = list[str]
    unique_letter_words = []

    with open("words.txt") as f:
        words = f.read().split("\n")

    for word in words:
        if len(bigger_then) > len(word):
            continue

        if has_unique_letters(word) == True:
            unique_letter_words.append(word)

    return unique_letter_words

def has_unique_letters(word: str):
    for i in word:
        for j in len(word):
            if i == j:
                pass
    return True

def new_unique_letters(input_word: str):
    from pathlib import Path

    longest = -1
    longest_word = ""

    words = Path("words.txt").read_text().split("\n")

    for word in words:
        if len(word) < longest:
            continue

    # ...


    # letters = {}
    # longest_word = ""
    #
    # for word in words:
    #     if len(word)

def main():
    #print(get_unique_letter_words("unpredictably"))

    pass

if __name__ == "__main__":
    main()