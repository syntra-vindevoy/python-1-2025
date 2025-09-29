#oefeningen B3-1.9.5
#(1) How many seconds are there in 42 minutes 42 seconds?
minutes = 42
seconds = 42

time = minutes * 60 + seconds
print(f"{time} seconds")

#(2) How many miles are there in 10 kilometers? Hint: there are 1.61 kilometers in a mile.
kilometers = 10
distance_miles = kilometers / 1.61
print(f"{distance_miles} miles")

#(3) If you run a 10-kilometer race in 42 minutes 42 seconds, what is your average pace in seconds per mile?
speed = kilometers / time
print(f"{speed}/s")

#(4) What is your average pace in minutes and seconds per mile?
time_for_kilometer = seconds / kilometers
#pace_in_miles = time_for_kilometer /

print(f"You travel 1 mile in {pace_in_miles} minutes and {time_for_kilometer} seconds. ")

#(5) What is your average speed in miles per hour?
