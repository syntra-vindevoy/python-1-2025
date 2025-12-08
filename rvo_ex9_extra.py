import numpy as np

import random


def binary_search(target, low=1, high=10000):
    steps = 0

    while low <= high:
        steps += 1
        mid = (low + high) // 2

        if mid == target:
            return steps  # klaar

        elif target < mid:
            high = mid - 1  # zoek in de lagere helft

        else:
            low = mid + 1  # zoek in de hogere helft

    return steps

def t_binary_search(runs=1000):
    max_steps = 0

    for _ in range(runs):
        target = random.randint(1, 10000)
        steps = binary_search(target)

        if steps > max_steps:
            max_steps = steps

    return max_steps


def main():
    randominteger = np.random.randint(low = 1, high = 10000)
    print(randominteger)
    steps = binary_search(1, low=1, high=10000)
    print(steps)
    print(t_binary_search(runs=1000))

if __name__ == '__main__':
    main()
