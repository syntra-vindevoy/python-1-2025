from dataclasses import replace
from datetime import datetime

def reverse_sentence(sentence:str):
    words = sentence.split()
    words = words.reverse()
    sentence = ' '.join(words)
    return sentence.capitalize()

def reverse_sentence2(sentence:str):
    return (" ".join(sentence.split()[::-1])).capitalize()

def total_length(test_amount:int):
    """Write a function called total_length that takes a list of strings and returns the total length of the strings.
    The total length of the words in word_list should be."""

    time_split = 0
    time_replace = 0
    time_ascii_sort = 0

    for i in range(test_amount):
        #TEST 1
        start_ts = datetime.now()
        with open ('words.txt', 'r') as file:
            content = file.read()
            content = content.split("\n")

            _ = len("".join(content))
        time_split = datetime.now() - start_ts

        #TEST 2
        start_ts = datetime.now()
        with open ('words.txt', 'r') as file:
            content = file.read()

            _ = len(content.replace("\n",""))

        time_replace = datetime.now() - start_ts

        #TEST 3
        start_ts = datetime.now()
        with open ('words.txt', 'r') as file:
            content = file.read()
            content = content.replace(ascii(" "),"").replace("\n", "")

            _ = len(content)
        time_ascii_sort = datetime.now() - start_ts

    print("-Count characters time" + "-"*8)
    print("Split:", time_split)
    print("Replace:", time_replace)
    print("Ascii sort:", time_ascii_sort)
    print("-"*30)

print(total_length(1))

def nested_sum(lst_ns:list = []):
    s = 0

    for l in lst_ns:
        for n in l:
            s += n
    return s

    for l in lst:
        s+= sum(l)

    return s

# def ns(lst: list[list]):
#     return sum([*l for l in lst])   #"Can't use starred expression here"    => List comprehension

# print(ns([1, 2], [3]))

def cumsum(lst:list[int]):
    cl = []
    count = 0

    for l in lst:
        count += l
        cl.append(count)

    return cl

def middle(lst_middle:list):
    return lst_middle[1:-1]

print(middle([1,2,3,4,5]))

def chop(lst_chop:list):
    lst_chop.pop(0)
    lst_chop.pop(-1)

lst = [1,2,3,4,5]
print(chop(lst))
print(lst)

def is_sorted(lst_sort:list) -> bool:
    # return sorted(lst) == lst   #Simple but not the best

    for i in range(1, len(lst_sort)):
        if lst_sort[i] > lst_sort[i-1]:
            return False
    return True

def cs(lst_cs:list):
    return [sum(lst[0:1]) for i in range(1, len(lst_cs) + 1)]

def has_duplicates(lst:list) -> bool:
    for i in range(lst):
        if lst[i] in lst[i+1:]:
            return True
    return False