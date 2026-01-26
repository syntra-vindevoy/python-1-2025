pairs = {}
seek = 15

numbers = [1, 6, 8, 4, 9, 7]

for index, number in enumerate(numbers):
    if (seek - number) in pairs:
        print(number, "on index", index, "is pair with", seek - number , "on index", pairs[seek - number])
        break

    pairs[number] = index


