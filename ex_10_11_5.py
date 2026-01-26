from ex10_11_2 import letter_count

def add_counters(word1, word2):
    counts_1 = letter_count(word1)
    counts_2 = letter_count(word2)

    for c in counts_2:
        #if c in counts_1:
        #    counts_1[c] += counts_2[c]
        #else:
        #    counts_1[c] = counts_2[c]

        counts_1[c] = counts_1.get(c, 0) + counts_2.get(c)

    return counts_1

def add_counters2(word1, word2):
    counts_1 = letter_count(word1)
    counts_2 = letter_count(word2)

    for k, v in counts_2.items():
        counts_1[k] = counts_1.get(k, 0) + v

    return counts_1


print(add_counters('brontosaurus', 'apatosaurus'))