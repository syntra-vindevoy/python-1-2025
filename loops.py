def my_function(x: int, y: int) -> int:
    while True:
        x+= 1

        if x > 5:
            break

    for letter in "Vindevogel":
        if letter == "i":
            continue

        print(letter)

my_function(x=-1, y=0)