def my_function(x: int, y: int) -> int:
    if y == 0:
        return 0

    while True:
        x += 1

        if x > 5:
            break

    for letter in "Vindevogel":
        if letter == "i":
            continue

        print(letter)


my_function(-1)