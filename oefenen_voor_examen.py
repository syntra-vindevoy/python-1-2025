from random import randint


def nested_sum(lst) -> int:
    counter = 0
    for item in lst:
        if isinstance(item, list):
            counter += nested_sum(item)

        elif isinstance(item, dict):
            counter += nested_sum(list(item.values()))

        elif isinstance(item, set):
            counter += nested_sum(list(item))

        elif isinstance(item, int):
            counter += item

        elif isinstance(item, str):
            raise ValueError("Strings are not allowed")

    return counter

def cumsum(lst:list) -> list:
    if not lst:
        return []
    counter = lst[0]
    return_list = [counter]

    for item in lst[1:]:
        counter = counter + item
        return_list.append(counter)

    return return_list

def middle(lst:list) -> list:
    return lst[1:-1]

def chop(lst:list):
    if not lst:
        return
    if len(lst)==1:
        lst.pop(0)
    elif len(lst)==2:
        lst.pop(0)
        lst.pop(0)
    else:
        lst.pop(0)
        lst.pop(-1)

def chop2(lst: list):
    del lst[:1]
    del lst[-1:]

def is_sorted(lst: list) -> bool:
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    return True

def is_sorted_oneline(lst):
    return all(lst[i] <= lst[i + 1] for i in range(len(lst) - 1))

def is_sorted_zip(lst: list) -> bool:
    return all(a <= b for a, b in zip(lst, lst[1:]))

def anagram(word1: str, word2: str) -> bool:
    word1 = word1.lower()
    word2 = word2.lower()
    return sorted(word1) == sorted(word2)

def has_duplicates(lst: list) -> bool:
    return len(set(lst)) != len(lst)

def birthday_paradox(number: int) -> bool:
    birthdays = [randint(1,365) for _ in range(number)]
    return len(set(birthdays)) != len(birthdays)

def words_to_list() -> list:
    lst = []
    with open("words.txt", "r") as f:
        for line in f:
            lst.append(line.strip())
    return lst

def in_bisect(word: str, lst: list, counter=1) -> tuple[bool, int]:
    if not lst:
        return False, counter - 1  # no match, steps taken

    middle = len(lst) // 2

    if lst[middle] == word:
        return True, counter
    elif word < lst[middle]:
        return in_bisect(word, lst[:middle], counter + 1)
    else:
        return in_bisect(word, lst[middle + 1:], counter + 1)



def main():
    print(nested_sum([[1,2],[3,4],{"a":5,"b":6} ]))
    print(cumsum([1,2,3]))
    print(middle([1,2,3,4,5]))
    lst = [1,2,3,4,5]
    #chop2(lst)
    #print(lst)
    print(is_sorted(lst))
    print(is_sorted_oneline(lst))
    print(is_sorted_zip(lst))
    counter = 0
    simulations = 50
    for _ in range(simulations):
        if birthday_paradox(23):
            counter += 1
    print(counter/simulations*100)
    lst = words_to_list()
    print(in_bisect("apple", lst))



if __name__ == '__main__':
    main()

