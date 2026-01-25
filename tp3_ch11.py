def is_newer_own(v1:str, v2:str) -> bool:
    #Code would not work as a list cannot handle 2 or more different types of values.
    l1 = v1.split(".")
    l2 = v2.split(".")
    # for i in range(len(l1)):
    #     if l1[i].isdigit():
    #         l1[i] = int(l1[i])
    #
    # for i in range(len(l2)):
    #     if l2[i].isdigit():
    #         l2[i] = int(l2[i])

    return False

def is_newer(v1, v2):
    # Remove parentheses and split version strings into parts
    # Example: "(2.a)" → ["2", "a"]
    v1 = v1.strip("()").split(".")
    v2 = v2.strip("()").split(".")

    # Make both versions the same length by padding with "0"
    # This allows comparison like "1.2" vs "1.2.0"
    max_len = max(len(v1), len(v2))
    v1 += ["0"] * (max_len - len(v1))
    v2 += ["0"] * (max_len - len(v2))

    # Compare each part of the versions one by one
    for p1, p2 in zip(v1, v2):

        # Case 1: Both parts are numbers
        # Compare numerically (e.g., 10 > 2)
        if p1.isdigit() and p2.isdigit():
            if int(p1) != int(p2):
                return int(p1) > int(p2)

        # Case 2: Both parts are letters
        # Compare alphabetically (e.g., "b" > "a")
        elif p1.isalpha() and p2.isalpha():
            if p1 != p2:
                return p1 > p2

        # Case 3: One part is a number and the other is a letter
        # Numbers are considered newer than letters
        # We do NOT compare number to letter directly
        else:
            return p1.isdigit()

    # If all parts are equal, v1 is not newer than v2
    return False



def main():
    assert is_newer("2", "1") is True
    assert is_newer("2.1", "1.2") is True
    assert is_newer("2.1.1", "2.1.0") is True
    assert is_newer("2.1.1", "10.1.0") is False
    assert is_newer("1.b", "1.a") is True

if __name__ == "__main__":
    main()