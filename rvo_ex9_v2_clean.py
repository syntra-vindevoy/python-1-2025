import numpy as np
from datetime import datetime as dt


# -----------------------------
# Basic List and String Utilities
# -----------------------------

def nested_sum(seq):
    """Return the sum of all numbers in a list of lists."""
    return sum(sum(item) for item in seq)


def cumsum(seq):
    """Return cumulative sum of the list."""
    total = 0
    result = []
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


def is_sorted_optimal(seq):
    """Return True if sequence is sorted, optimized check."""
    return all(seq[i] >= seq[i - 1] for i in range(1, len(seq)))


def is_anagram(a, b):
    """Return True if two words are anagrams."""
    return sorted(a) == sorted(b)


def has_duplicates(seq):
    """Return True if list contains duplicates."""
    return len(seq) > len(set(seq))


# -----------------------------
# Birthday Paradox
# -----------------------------

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


# -----------------------------
# Word List Utilities
# -----------------------------

def load_words(path='words.txt'):
    """Load word list into both a list (order preserved) and a set (fast lookups)."""
    with open(path) as f:
        words = [line.strip() for line in f]
    return words, set(words)


def reverse_pairs(words, word_set):
    """Return list of words whose reverse is also a word."""
    return [w for w in words if w[::-1] in word_set]


# -----------------------------
# Interlock Functions
# -----------------------------

def interleave(w1, w2):
    """Interleave two words of the same length."""
    if len(w1) != len(w2):
        return None
    return ''.join(a + b for a, b in zip(w1, w2))


def find_interlocking_pairs(word_list, word_set):
    """Find all pairs (w1, w2) that interlock to form a valid word."""
    results = []
    for word in word_list:
        if len(word) < 2:
            continue
        w1 = word[::2]
        w2 = word[1::2]
        if w1 in word_set and w2 in word_set:
            results.append((w1, w2, word))
    return results


def find_three_way_interlocks(word_list, word_set):
    """Find all 3-way interlocking words."""
    results = []
    for word in word_list:
        if len(word) < 3:
            continue
        w1 = word[0::3]
        w2 = word[1::3]
        w3 = word[2::3]
        if w1 in word_set and w2 in word_set and w3 in word_set:
            results.append((w1, w2, w3, word))
    return results


# -----------------------------
# Main Execution
# -----------------------------

def main():
    # Basic function tests
    print("Nested sum:", nested_sum([[1, 2], [3], [4, 5, 6]]))
    print("Cumulative sum:", cumsum([1, 2, 3]))
    print("Middle:", middle([1, 2, 3, 4]))

    t = [1, 2, 3, 4]
    chop(t)
    print("Chopped:", t)

    print("Is sorted:", is_sorted(['b', 'a']))
    print("Is sorted optimal:", is_sorted_optimal(['a', 'b']))
    print("Anagram check:", is_anagram('brak', 'krab'))
    print("Has duplicates:", has_duplicates([1, 2, 3, 4, 5]))
    print("Birthday simulation:", simulate_birthdays(1000))

    # Load word list
    print("\nLoading words...")
    word_list, word_set = load_words()
    print(f"Loaded {len(word_list)} words.")

    # Reverse pairs
    print("\nReverse pairs:")
    for w in reverse_pairs(word_list, word_set):
        print(f"{w} ↔ {w[::-1]}")

    # Two-way interlocked words
    print("\nTwo-way interlocked words:")
    inter2 = find_interlocking_pairs(word_list, word_set)
    for w1, w2, combined in inter2:
        print(f"{combined} = {w1} + {w2}")

    # Three-way interlocked words
    print("\nThree-way interlocked words:")
    inter3 = find_three_way_interlocks(word_list, word_set)
    for w1, w2, w3, combined in inter3:
        print(f"{combined} = {w1} + {w2} + {w3}")


if __name__ == '__main__':
    main()
