#oefeningen B3_1-9-5
#(1) How many seconds are there in 42 minutes 42 seconds?
minutes = 42
seconds = 42

time = minutes * 60 + seconds
print(f"{time} seconds")

#(2) How many miles are there in 10 kilometers? Hint: there are 1.61 kilometers in a mile.
kilometers = 10
KILOMETERS_PER_MILES = 1.61
distance_miles = kilometers / KILOMETERS_PER_MILES
print(f"{distance_miles} miles")

#10km/42min42sec -> miles/sec -> 10/1.6 & 42 * 60 + 42 -> 16.1miles/2562sec -> (miles/miles) / (sec/miles)
#(3) If you run a 10-kilometer race in 42 minutes 42 seconds, what is your average pace in seconds per mile?
pace_per_miles = time/distance_miles
print(f"{pace_per_miles}/miles")

#(4) What is your average pace in minutes and seconds per mile?
pace_minutes = pace_per_miles // 60
pace_seconds = pace_per_miles % 60
print(f"You travel 1 mile in {pace_minutes} minutes and {pace_seconds} seconds")

#(5) What is your average speed in miles per hour?
# miles/sec
#speed_per_hour = pace_per_miles / ( * 60 * 60)

# KILOMETERS_PER_KILOMETERS = 1.61
#
# def convert_miles_to_kilometers(miles):
#....