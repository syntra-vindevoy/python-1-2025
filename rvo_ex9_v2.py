def nested_sum(l):
    total = 0
    for item in l:
        total += sum(item)
    return total
# return sum([sum(l) for l in list])

def cumsum(l):
    lst = []
    total = 0
    for item in l:
        total += item
        lst.append(total)
    return lst

def middle(l):
    return l[1:-1]

def chop(lst):
    lst.pop(0)
    lst.pop(-1)

def is_sorted(lst):
    l = sorted(lst)
    return lst == l

def is_sorted_optimal(lst):

    for i in range(1, len(lst)):
        if lst[i] < lst[i-1]: #je gaat niet heel de lijst door moeten lopen hier mee
            return False
    return True

def is_anagram(word1, word2):
    word1 = sorted(word1)
    word2 = sorted(word2)
    return word1 == word2

def has_duplicates(lst):
    for i in range(len(lst)):
        if lst[i] in lst[i+1:]:
            return True
    return False

def has_duplicates_optimal(lst):
    lst = sorted(lst)
    for i in range(0, len(lst)-1):
        if lst[i] == lst[i+1]:
            return True
    return False

def has_duplicates_best(lst):
    return len(lst) > len(set(lst))

def random_bdays(n):
    """Returns a list of integers between 1 and 365, with length n.

    n: int

    returns: list of int
    """
    import numpy as np
    t = []
    for i in range(n):
        bday = np.random.randint(1, 365)
        t.append(bday)
    return t

def simulate_birthdays(n):
    counter = 0
    for _ in range(n):
        bdays = random_bdays(23)
        if has_duplicates(bdays):
            counter += 1
    return counter/n
LOW = 1
HIGH = 10000
def bisection(r, low=LOW, high=HIGH):
    medium = (low + high) // 2
    counter = 1
    if r == medium:
        return counter
    while r != medium:
        if r < medium:
            high = medium+1
        else:
            low = medium-1
        medium = (low + high) // 2
        counter += 1
    return counter

def list_from_words_v1():
    lst = []
    with open('words.txt') as f:
        for line in f:
            line = line.strip()
            lst.append(line)
    return lst

def list_from_words_v2():
    lst = []
    with open('words.txt') as f:
        for line in f:
            line = line.strip()
            lst = lst + [line]
    return lst

def reverse_pair(lst):
    reversed_lst = []
    for l in lst:
        if l[::-1] in lst:
            reversed_lst.append(l)
    return reversed_lst

def interlocked(word_set, word):

    w1 = word[::2]
    w2 = word[1::2]
    return w1 in word_set and w2 in word_set


def interlock_general(word_set, word, n=3):

    for i in range(n):
        part = word[i::n]
        if part not in word_set:
            return False
    return True


"""
Utility functions + wordlist operations + interlock detection.

Improved and optimized rewrite.
"""

import numpy as np


# -------------------------------------------------
# Basic list and string utilities
# -------------------------------------------------

def nested_sum(seq):
    """Return the sum of all numbers in a list of lists."""
    total = 0
    for item in seq:
        total += sum(item)
    return total


def cumsum(seq):
    """Return cumulative sum of the list."""
    result = []
    total = 0
    for x in seq:
        total += x
        result.append(total)
    return result


def middle(seq):
    """Return list without first and last element."""
    return seq[1:-1]


def chop(seq):
    """Remove first and last elements in-place."""
    if len(seq) >= 2:
        seq.pop(0)
        seq.pop(-1)


def is_sorted(seq):
    """Return True if sequence is sorted."""
    return seq == sorted(seq)


def is_anagram(a, b):
    """Return True if two words are anagrams."""
    return sorted(a) == sorted(b)


def has_duplicates(seq):
    """Return True if list contains duplicates."""
    for i in range(len(seq)):
        if seq[i] in seq[i + 1:]:
            return True
    return False


# -------------------------------------------------
# Birthday paradox
# -------------------------------------------------

def random_bdays(n):
    """Return a list of n random birthdays (1–365)."""
    return list(np.random.randint(1, 365, size=n))


def simulate_birthdays(trials):
    """Simulate probability of shared birthdays in groups of 23."""
    matches = 0
    for _ in range(trials):
        if has_duplicates(random_bdays(23)):
            matches += 1
    return matches / trials


# -------------------------------------------------
# Word list utilities
# -------------------------------------------------

def load_words(path='words.txt'):
    """Load word list into both a list (order preserved) and a set (fast lookups)."""
    with open(path) as f:
        lst = [line.strip() for line in f]
    return lst, set(lst)


def reverse_pairs(words, word_set):
    """Return list of words whose reverse is also a word."""
    return [w for w in words if w[::-1] in word_set]


# -------------------------------------------------
# Interlock functions
# -------------------------------------------------

def interlocked(word_set, word):
    """Two-way interlock: even+odd letters form valid words."""
    w1 = word[::2]
    w2 = word[1::2]
    return w1 in word_set and w2 in word_set


def interlock_general(word_set, word, n=3):
    """General n-way interlock."""
    for i in range(n):
        part = word[i::n]
        if part not in word_set:
            return False
    return True


def bisection_list(word_list, target):
    """
    Binary search using the same structure and style
    as the user's original `bisection` function.

    Returns True if `target` is in `word_list`.
    """
    low = 0
    high = len(word_list) - 1

    while low <= high:
        mid = (low + high) // 2
        word = word_list[mid]

        if word == target:
            return True
        elif target < word:
            high = mid - 1
        else:
            low = mid + 1

    return False

def interlocked(word_list, word):
    w1 = word[::2]
    w2 = word[1::2]
    return bisection_list(word_list, w1) and bisection_list(word_list, w2)

def interlock_general(word_list, word, n=3):
    for i in range(n):
        part = word[i::n]
        if not bisection_list(word_list, part):
            return False
    return True


# -------------------------------------------------
# Main execution
# -------------------------------------------------

def main():
    from datetime import datetime as dt

    # Basic function tests
    print(nested_sum([[1, 2], [3], [4, 5, 6]]))
    print(cumsum([1, 2, 3]))
    print(middle([1, 2, 3, 4]))

    t = [1, 2, 3, 4]
    chop(t)
    print(t)

    print(is_sorted(['b', 'a']))
    print(is_sorted_optimal(['a', 'b']))

    print(is_anagram('brak', 'krab'))
    print(has_duplicates([1, 2, 3, 4, 5]))
    print(simulate_birthdays(1000))
    """
    # Load words
    print("\nLoading word list...")
    start = dt.now()
    word_list, word_set = load_words()
    print("Loaded in:", dt.now() - start)

    # Reverse pairs
    print("\nReverse pairs:")
    for w in reverse_pairs(word_list, word_set):
        print(f"{w} ↔ {w[::-1]}")

    # Two-way interlocked words
    print("\nTwo-way interlocked words:")
    for word in word_list:
        if interlocked(word_set, word):
            w1 = word[::2]
            w2 = word[1::2]
            print(f"{word} = {w1} + {w2}")

    # Three-way interlocked words
    print("\nThree-way interlocked words:")
    for word in word_list:
        if interlock_general(word_set, word, 3):
            w1 = word[0::3]
            w2 = word[1::3]
            w3 = word[2::3]
            print(f"{word} = {w1} + {w2} + {w3}")
    """


if __name__ == '__main__':
    main()