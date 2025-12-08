LOW = 1
HIGH = 10000000

def bisection_search(number, low: LOW, high: HIGH):
    medium = 0
    count = 1

    while number != medium:
        medium = (low + high) // 2

        if number < medium:
            high = medium - 1

        else:
            low = medium + 1

        count += 1

    return count

def main():
    max_searches = 0
    max_number = 0

    for number in range(LOW, HIGH + 1):
        searches = bisection_search(number, LOW, HIGH)

        if searches > max_searches:
            max_searches = searches
            max_number = number

    print(max_searches, "searches needed for", max_number)


if __name__ == "__main__":
    main()
