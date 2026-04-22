from pathlib import Path
import math
def anagrams():
    words = Path('words.txt').read_text().splitlines()
    dictionary = {}
    for word in words:
        word_sorted = sorted(word.lower())
        word_sorted = "".join(word_sorted)
        dictionary[word_sorted] = dictionary.get(word_sorted, 0) + 1
    maximum = max(dictionary.values())
    return [kv for kv in dictionary.items() if kv[1] == maximum]

cache = {2: True}

def priemgetal(number, cache):
    if number < 2:
        return False
    if number in cache:
        return cache[number]

    limit = int(math.sqrt(number))

    for i in range(2, limit+1):
        if i not in cache:
            priemgetal(i, cache)

    for p, is_prime in cache.items():
        if is_prime and p <= limit:
            if number % p == 0:
                cache[number] = False
                return False

    cache[number] = True
    return True

def complement_15(lst:list):
    check = {}
    for item in lst:
        print(item)
        print(check.keys())
        if 15-item in check:
            return item, check[15-item]
        else:
            check.update({item: item})


def main():
    print(anagrams())
    print(priemgetal(2,cache))
    print(priemgetal(3,cache))
    print(cache)
    print(priemgetal(139,cache))
    print(cache)
    lst = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    print(complement_15(lst))

if __name__ == '__main__':
    main()