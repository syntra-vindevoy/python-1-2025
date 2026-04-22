from pathlib import Path
def interlocking():
    words = Path("words.txt").read_text().splitlines()
    words_dict = {k: v for v,k in enumerate(words)}
    interlock = {}
    for word in words:
        first = word[0::2]
        second = word[1::2]
        if first in words_dict.keys() and second in words_dict.keys():
            interlock.update({word:[first,second]})
    return interlock

def interlocking2(word):
    words = Path("words.txt").read_text().splitlines()
    words_dict = {k: v for v,k in enumerate(words)}
    first = word[0::2]
    second = word[1::2]
    if word in words_dict.keys() and first in words_dict.keys() and second in words_dict.keys():
        return [word, first, second]
    else:
        return []

def main():
    word = 'schooled'
    print(interlocking())
    #print(interlocking2(word))

if __name__ == '__main__':
    main()
