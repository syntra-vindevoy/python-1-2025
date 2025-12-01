#You can put anything in the []-list, the type won't be locked to the type of the first value
import datetime

l = ["Yves", "Niels"]
l = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
l = ["Yves", 1972, ["haha", 17.5]]  #[]-list accepts multiple types.
#l = list("Yves", 1972) #A ()-list accepts only 1 type.

#Empty lists
#l = list[] #Doesn't work
l = []
l = list()
l = ()

#None is accepted in a list
l = [None, 5, 7]    #None is for shoving the rest of the values up in order, so you can count from 1-.. instead of 0-.. where you
#_ is a normal variable
for _ in range(3):  #_ is used when you need a variable name that you won't use again, unlike an i (iteration/index)
    print()

#[]-lists are mutable
#()-lists are immutable

#Check if the value is in the list.
if "Brent" in l:
    print(True)

#Slicing
letters = ['a', 'b', 'c', 'd']
print(letters[1:3])
#Prints:    ['b', 'c']

print(range(0,4))   #Prints     range(0,4)  Because "range()" is it's own class
print(list(range(0,4)))   #Prints  [0, 1, 2, 3]  Because "range()" got converted to a list, which print prints it like so.

l1 = [1, 2]
l2 = [3, 4]
print(l1 +l2)   #Prints the first list + the second list. Does not add them together like math, it becomes [1, 2, 3, 4].

#CLASSIC MISTAKES
t1 = ["test1", "test2"]
t2 = ["test3", "test4"]

print(t1.append(t2))    #Adds the second list as type list to the first list. prints: [test1, test2, [test3, test4]]
t1 = t1.append("test5") #The function append already adds the value, but then returns "None", wich you then pass to t1 setting t1 to value None, removing the list.

def time_test_plus_extend():
    start = datetime.datetime.now()

    for i in range(100000):
        t3 = t1 + t2

    end = datetime.datetime.now()
    print(end - start)

    start = datetime.datetime.now()

    for i in range(100000):
        t1.extend(t2)

    end = datetime.datetime.now()
    print(end - start)

names = ["Yves", "Niels"]
print(names.pop(0))
print(names.remove("Niels"))    #Print is useless to print since .remove is a void function that returns None
print(names)

del names[0]    #Del comes from "delete", deletes only from mutables, normal variables are immutable like strings, so can't use del

names = sorted(names)   #returns the sorted list, so you need to put it somewhere.
names.sort()            #Is a void, returns nothing.

def making_word_list(): #9.12
    word_list = []

    for line in open("words.txt"):
        word = line.strip()
        word_list.append(word)
    print(len(word_list))