def read_wordlist() -> dict:
    return_data = dict()
    with open("words.txt") as f:
        for line in f:
            line = line.strip()
            return_data.update({line: 1})
    return return_data

def check_wordlist(wordlist: dict, word: str) -> bool:
    if word in wordlist:
        return True
    else:
        return False

def main():
    words = read_wordlist()
    word = 'apple'
    print(check_wordlist(words, word))

if __name__ == '__main__':
    main()
