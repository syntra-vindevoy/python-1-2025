def factorial_apart(n):
    # if n < 0:
    #     print("n must be greater than 0")# dit is fout hé
    #     return
    #dit is fout hé, niet printen in de functie
    assert n > 0, "n must be > 0"
    if n == 0:
        return 1
    return n * factorial_apart(n-1)

try:
    print(factorial_apart(-1))
except Exception as e:
    print(("Error occurred: ") + str(e))