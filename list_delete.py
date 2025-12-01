import string
import time
import functools

REPEAT = 1
STATES = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]

STRIPPED = [
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]

with open("words.txt", "r") as f:
    WORDS = f.read().splitlines()

#WORDS = WORDS * 10

def timed_repeater(repeat):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = None
            for _ in range(repeat):
                result = func(*args, **kwargs)
            end = time.time()
            # arg_list = []
            # if args:
            #     arg_list.extend(repr(a) for a in args)
            # if kwargs:
            #     arg_list.extend(f"{k}={v!r}" for k, v in kwargs.items())
            # params_str = ", ".join(arg_list)
            # print(f"{func.__name__}({params_str}) executed {repeat} times in {end - start:.6f} seconds")
            print(f"{func.__name__} executed {repeat} times in {end - start:.6f} seconds")
            return result


        return wrapper
    return decorator


@timed_repeater(repeat=REPEAT)
def with_remove(lst: list[str]):
    for item in lst[:]:
        if item[0].upper() in {"A", "E", "I", "O", "U"}:
            lst.remove(item)

    return lst

@timed_repeater(repeat=REPEAT)
def with_pop(lst: list[str]):
    for index in range(len(lst) - 1, -1, -1):
        if lst[index][0].upper() in {"A", "E", "I", "O", "U"}:
            lst.pop(index)

    return lst

@timed_repeater(repeat=REPEAT)
def with_del(lst: list[str]):
    items = lst[:]

    for index in range(len(items) - 1, -1, -1):
        if items[index][0].upper() in {"A", "E", "I", "O", "U"}:
            del items[index]

    return items

@timed_repeater(repeat=REPEAT)
def with_list_comp(lst: list[str]):
    return [i for i in lst if i[0].upper() not in {"A", "E", "I", "O", "U"}]


@timed_repeater(repeat=REPEAT)
def with_list_copy(lst: list[str]):
    result = []

    for item in lst:
        if item[0].upper() not in {"A", "E", "I", "O", "U"}:
            result.append(item)

    return result


@timed_repeater(repeat=REPEAT)
def with_dict(lst: list[str]):
    d: dict = {l:[] for l in string.ascii_uppercase}

    for item in lst:
        fl = item[0].upper()
        d[fl].append(item)

    for v in {"A", "E", "I", "O", "U"}:
        d.pop(v)

    return [item for items in d.values() for item in items]

@timed_repeater(repeat=REPEAT)
def with_reduce(lst: list[str]):
    d = functools.reduce(
        lambda acc, item: (acc[item[0].upper()].append(item), acc)[1],
        lst,
        {l: [] for l in string.ascii_uppercase}
    )

    for v in {"A", "E", "I", "O", "U"}:
        d.pop(v)

    return [item for items in d.values() for item in items]


def main():
    print("ALL STATES")
    stripped = with_remove(STATES)
    assert stripped == STRIPPED

    stripped = with_pop(STATES)
    assert stripped == STRIPPED

    stripped = with_del(STATES)
    assert stripped == STRIPPED

    stripped = with_list_comp(STATES)
    assert stripped == STRIPPED

    stripped = with_list_copy(STATES)
    assert stripped == STRIPPED

    stripped = with_dict(STATES)
    assert stripped == STRIPPED

    stripped = with_reduce(STATES)
    assert stripped == STRIPPED

    print("20 STATES")
    with_remove(STATES[:20])
    with_pop(STATES[:20])
    with_del(STATES[:20])
    with_list_comp(STATES[:20])
    with_dict(STATES[:20])
    with_reduce(STATES[:20])


    print("5 STATES")
    with_remove(STATES[:5])
    with_pop(STATES[:5])
    with_del(STATES[:5])
    with_list_comp(STATES[:5])
    with_dict(STATES[:5])
    with_reduce(STATES[:5])

    print("WORDS")
    # with_remove(WORDS)
    with_pop(WORDS)
    with_del(WORDS)
    with_list_comp(WORDS)
    with_list_copy(WORDS)
    with_dict(WORDS)
    with_reduce(WORDS)

if __name__ == "__main__":
    main()
