#Lesson taught using page: https//:w3schools.com/python/python_red_string.asp

fruit = "banana"
i = -1
for i in range(len(fruit)):
    print(fruit[i])

print(fruit[2])     #Print the singular letter of fruit 2nd position
#print(fruit[10])    #Throws error since there aren't 10 letters in fruit (gives error)
print(fruit[0:5])   #Print fruit from 0th position, to the 5th position
print(fruit[0:10])  #Print fruit from 0th position, to the 10th position, even though it doesn't have 10 letters (no error)
print(fruit[0:])    #Print fruit from 0th position, to the NONE-th position, and so prints till it finds a NONE (no letter, end of word)(no error)
print(fruit[:])     #Print fruit from NONE-th position, to the NONE-th position, and so prints from beginning until it finds a NONE (no letter, end of word)(no error)
print(fruit[::-1])  #Print fruit from NONE-th position, to the NONE-th position, but steps in reverse, so prints the inverse of the fruit(no error)
# fruit[START_POSITION:END_POSITION:ITERATION_STEP]       nothing required in between, template = [:], max length = [::], filled example = [1,3,-1]
#       |> if none then start at beginning
#                       |> if none then end at end
#                                   |> if none then second : is not needed and is thus 1 standerd
#                                   |> if -1, step in reverse

print()
print("STRING COMPARE", end="\n\n")#STRING COMPARE
print("banana" < "Bananas") #Here it doesn't compare length (use len()), it compares ASCII character per character
                            #0 comes before and is thus smaller than 1, A in the table comes before a and is thus smaller.
                            #the first letter of "banana" comes after the first letter of "Bananas" and so, banana is bigger than "Bananas"

#Always use YYYY-MM-DD as standerd with the dash in between
print("2025-11-10")

#This way compares well
print("2025-11-10" < "2025-11-11")

#This way compares the first character and then sort when there's a difference,
#but here smaller days are compared first, even in a years difference, it could be wrong.
print("10-11-2025" < "11-11-2024")

#Here a dash isn't used, so a shortened annotation like first day of month.
#(01/02/2025 becomes 1/2/2025)(2025 could become '25, 01-01-2025 becomes 1-1-25 then 1125, obviously different from 01012025)
print("112025" < "02032025") #Checks as string, not as int
print(112025 < 2032025) #Checks as int, not as string

#ASCII
"""
Weird symbols? Save as UTF-16.
Basic but with €? Save as UTF-15.
Most basic? Save as UTF-8.
First MOST basic? Save as UTF-1.
"""

print()
import uuid
print("-10".isdigit())

#Gebruik uuid4 als ID dat niet makkelijk te vinden is in een publieke API
print(uuid.uuid4())
#Gebruik uuid7 als ID dat niet makkelijk te vinden is in een publieke API EN je eerst kunt sorteren op de eerste groep.
print(uuid.uuid5(uuid.uuid4(), "testing"))   #Python doesn't seem to have uuid7 since it could have a fault. The Internet advises to use uuid5, Yves said to use uuid7.

#IP
ip = [127, 0, 0, 1]
private_ip = [10, 0, 0, 1]
