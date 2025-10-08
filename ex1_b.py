KILOMETERS_TO_MILE = 1.61


def convert_kilometers_to_miles(kilometers: float) -> float:
    return kilometers / KILOMETERS_TO_MILE


def convert_miles_to_kilometers(miles: float) -> float:
    return miles * KILOMETERS_TO_MILE


def main():
    assert convert_kilometers_to_miles(1) == 1 / KILOMETERS_TO_MILE
    assert convert_miles_to_kilometers(1) == 1.61


if __name__ == "__main__":
    main()


# minutes= 42
# seconds = 42
#
# total_seconds = minutes * 60 + seconds
# print(total_seconds)
#
#
#
# kms = 10
# miles = KILOMETERS_TO_MILE * kms
# print(kms, "km is gelijk aan", miles, "mijlen")
#
# distance_km = 10
# minutes = 42
# seconds = 42
# total_seconds = minutes * 60 + seconds
# distance_miles = distance_km / KILOMETERS_TO_MILE
# print("distance mijlen", distance_miles)
#
# pace = total_seconds / distance_miles
# print(pace)
#
# pace = round(pace, 3)
#
# pace_minutes = pace // 60
# print(pace_minutes)
# pace_seconds = pace % 60
# print(pace_seconds)
#
# pace = (1 / pace * 60 * 60)
# print(pace)
