minutes = 42
seconds = 42

total_seconds = minutes * 60 + seconds
print(total_seconds)


KILOMETERS_TO_MILE = 1.61

kms = 10
miles = KILOMETERS_TO_MILE * kms
print(kms, "km is gelijk aan", miles, "mijlen")

distance_km = 10
minutes = 42
seconds = 42
total_seconds = minutes * 60 + seconds
distance_miles = distance_km / KILOMETERS_TO_MILE
print("distance mijlen", distance_miles)

pace = total_seconds / distance_miles
print(pace)

pace = round(pace, 3)

pace_minutes = pace // 60
print(pace_minutes)
pace_seconds = pace % 60
print(pace_seconds)

pace = 1 / pace * 60 * 60
print(pace)
