def main():
    seconds = 42
    minutes = 42
    hours = 0
    days = 0
    years = 0  # define variables
    print(convert_to_seconds(years, days, hours, minutes, seconds))


def convert_to_seconds(y, d, h, m, s):
    time_in_seconds = (
        s + m * 60 + h * 3600 + d * 24 * 3600 + y * 365 * 24 * 3600
    )  # this is a function that calculates time in seconds
    return time_in_seconds


if __name__ == "__main__":
    main()

KILOMETERS_TO_MILE = 1.61  # capital letters because it is a global variable
kms = 10
miles = kms / KILOMETERS_TO_MILE
print(kms, " km is gelijk aan", miles, "mijlen")

distance = 10
time = 42 + 42 * 60
distance_miles = distance / KILOMETERS_TO_MILE
print(" miles is gelijk aan", distance_miles)
average_pace = time / distance_miles
print(average_pace)
pace_minutes = average_pace // 60
pace_seconds = average_pace % 60
print(pace_minutes)
print(pace_seconds)

average_pace_invert = 1 / average_pace
print(average_pace_invert)

average_pace_invert_mpu = average_pace_invert * 3600
print(average_pace_invert_mpu)
