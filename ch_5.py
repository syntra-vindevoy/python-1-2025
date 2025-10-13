def wrong_code(number:int):
    if number >= 0:
        return True
    else:
        return False
def good_code(number:int):
    return number >= 0

def main():
    if wrong_code(5):
        print("Positive number")
    else:
        print("Negative number")

    if good_code(5):
        print("Positive number")
    else:
        print("Negative number")

    print(f"{'Positive' if good_code(5)  else 'Negative'} number")

if __name__ == "__main__":
    main()