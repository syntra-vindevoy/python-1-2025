def find_doubles():
    with open("words.txt") as f:
        lines = f.readlines()

    for w in lines:
        word = w.strip()
        previous = ""
        #for c in word: #De for gebruiken voor letter per letter te checken kan niet door een letter niet te kunnen overslaan.
        for l in word: #checkt laatste letter ookal is het nooit nodig
            if word[i] == word[i + 1]:


def is_triple_double(word):
    i = 0
    count = 0
    while i < len(word) - 1:
        if word[i] == word[i + 1]:
            count = count + 1
            if count == 3:
                return True
            i = i + 2
        else:
            i = i + 1 - 2 * count
            count = 0
    return False

def find_triple_double():
    fin = open('words.txt')
    for line in fin:
        word = line.strip()
        if is_triple_double(word):
            print(word)


def main():
    pass

if __name__ == "__main__":
    main()