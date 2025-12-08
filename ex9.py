def reverse_sentence(sentence):
    words = sentence.split()[::-1]
    words = words.reverse()
    sentence = ' '.join(words)
    return sentence.capitalize()

    # return (" ".join(sentence.split()[::-1])).capitalize()

def total_length():
    #length = 0
    #
    #with open("words.txt") as f:
    #    for line in f:
    #        line = line.strip()
    #        length += len(line)
    #
    #return length

    with open("words.txt") as f:
        content = f.read()
        content = content.split("\n")

        return len("".join(content))

    with open("words.txt") as f:
        content = f.read()

        return len(content.replace("\n", ""))


def nested_sum(lst: list[list]):
    s = 0

    for l in lst:
        for n in l:
            s += n

    return s

    for l in lst:
        s += sum(l)

    return s


def ns(lst: list[list]):
    return sum([sum(l) for l in lst])

print(ns([[1, 2], [3]]))


def cumsum(lst: list[int]):
    cl = []
    count = 0

    for l in lst:
        count += l
        cl.append(count)

    return cl

def cs(lst: list[int]):
    return [sum(lst[0:i]) for i in range(1, len(lst) + 1)]

def middle(lst: list):
    return lst[1:-1]

print(middle([1,2,3,4]))


def chop(lst: list):
    lst.pop(0)
    lst.pop(-1)

lst = [1,2,3,4]
print(chop(lst))
print(lst)

def is_sorted(lst: list) -> bool:
    #return sorted(lst) == lst

    for i in range(0, len(lst) -1):
        if lst[i] > lst[i+1]:
            return False

    return True


def has_duplicates(lst: list) -> bool:
    #for i in range(0, len(lst)):
    #    if lst[i] in lst[i+1:]:
    #        return True
    #
    #return False

    lst = sorted(lst)

    for i in range(0, len(lst) - 1):
        if lst[i] == lst[i+1]:
            return True

    return False

    for element in lst:
        if lst.count(element) > 1:
            return True

    return len(lst) > len(set(lst))