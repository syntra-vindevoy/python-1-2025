import random
import math

# 1) Zoek de woorden met anagrammen, sommige woorden hebben meerdere anagrammen, lijst ze op, en sorteer op meest tot minst.
def is_anagram(word1: str, word2: str) -> bool:
    return sorted(word1.lower()) == sorted(word2.lower())

from pathlib import Path
def ex1():
    words = Path("words.txt").read_text().splitlines()
    counts = {}

    for word in words:
        s = str(sorted(word))

        if s in counts:
            counts[s].append(word)
        else:
            counts[s] = [word]

    counts = sorted(counts.items(), key=lambda x: len(x[1]), reverse=True)
    max_ana = len(counts[0][1])
    counts = {k:v for k,v in counts if len(v) == max_ana}
    print(max_ana)
    print(counts)


# 2) Priemgetallen met caching (gebruik memos)
def priem_memos(retrieve):
    primes = []
    counter = 0
    check = 3
    retrieve = 100

    while counter < retrieve - 1:
        sqrt_check = math.sqrt(check)
        is_prime = True

        for prime in primes:
            if prime > sqrt_check:
                break

            if check % prime == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(check)
            counter += 1

        check += 2

    primes = [2] + primes

    print(primes)

def chapter_example(setn):
    known = {0: 0, 1: 1}

    def fibonacci_memo(n):
        if n in known:
            return known[n]

        res = fibonacci_memo(n - 1) + fibonacci_memo(n - 2)
        known[n] = res
        return res

    print(fibonacci_memo(setn))


# 3) Lijst met getallen, elk cijfer ligt tussen 0 en 10. Zoek een getal, dat met een ander getal 15 vormt (+-*/) allebei in de lijst.
#    Geen cijfer hergebruiken.
        #Pak het getal, doe dat getal (+-*/) met 15, en zoek het resultaat in de lijst.
def combo_to_number(goal_number:int, number_list:list[int]):
    combos = {} # {number_found, "formula"}
    #
    # for number in number_list:
    #     to_find = goal_number / number
    #     if to_find in number_list and to_find == number:
    #         pass


    #Individual calculations
    for i in range (len(number_list)):
        for j in range (len(number_list)):
            if j <= i:
                continue

            if goal_number == number_list[i] + number_list[j]:
                combos[number_list[i]] = number_list[j]
            if goal_number == number_list[i] - number_list[j]:
                combos[number_list[i]] = number_list[j]
            if goal_number == number_list[i] * number_list[j]:
                combos[number_list[i]] = number_list[j]
            if goal_number == number_list[i] / number_list[j]:
                combos[number_list[i]] = number_list[j]

    pass
def cto_setup():
    n_list = []
    for _ in range(random.randrange(5, 20)):
        n_list.append(random.randrange(1, 10))

    return n_list

def ex3():
    pairs = {}
    seek = 15

    numbers = [1, 6, 8, 4, 9, 7]

    for index, number in enumerate(numbers):
        if (seek - number) in pairs:
            print(number, "on index", index, "is pair with", seek - number, "on index", pairs[seek - number])
            break

        pairs[number] = index


def main():
    #Exercise 2 code
    # chapter_example(3)
    # priem_memos(100)
    #
    # primes = [2] + primes
    #
    # print(primes)
    #Exercise
    #combo_to_number(15, cto_setup()) #15, random length of random numbers 1->10
    print("End")

if __name__ == "__main__":
    main()