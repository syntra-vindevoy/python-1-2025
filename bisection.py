LOW = 1
HIGH= 10000

def bisection(number, low: LOW, high: HIGH):
    medium = (low + high) // 2
    count = 1
    if low == high:
        return count

    if number == medium:
        return count

    while number != medium:
        if number < medium:
            high = medium
        if number > medium:
            low = medium

        medium = (low + high) // 2
        count += 1
    return count

def main():
    import random

    max_searches = 0

    for nuber in range(LOW, HIGH + 1):
        number = random.randint(LOW, HIGH)
    r = random.randint(LOW, HIGH)
    print(r, "was found in", bisection(r, LOW, HIGH), "tries.")

if __name__ == "__main__":
    main()