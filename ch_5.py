def wrong_code(number:int):
    if number >= 0:
        return True
    else:
        return False
def good_code(number:int):
    return number >= 0

# Faculteit met "tail-end recursion"
def fac(n):
    def go(n, a):
        if n == 1:
            return a
        else:
            return go(n - 1, n * a)
    return go(n, 1)

def main():
    if wrong_code(5):
        print("Positive number")
    else:
        print("Negative number")

    if good_code(5):
        print("Positive number")
    else:
        print("Negative number")

    # Best code
    print(f"{'Positive' if good_code(5)  else 'Negative'} number")

    print(fac(5))
if __name__ == "__main__":
    main()