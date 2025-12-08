def ex_string_value_change():  #In short: strings are immutable
    a = "Brent"
    b = "Brent"

    # Both have the same type and value, but not the same place in memory.
    print(a)
    print(b)
    print("-------------")
    a = "Brent"
    b = a
    # b got the value of a, both then point to the same place in memory

    print(a)
    print(b)
    print("-------------")

    a = "Christian"
    # a is now changed. But but b does not change together with a. b still points to the last value it got (pointed to).
    print(a)
    print(b)
    print("-------------")
    print("-------------")

def ex_list_value_change(): #In short: lists are mutable
    l1 = [1, 2, 3]
    l2 = l1
    #The first list points to a place, that place has a list, and reads that list.
    #Same for l2, it gets pointed to the place l1 also saved, that place has a list.
    #l1 points to a place. l2 points to a place. They both point to the same place in memory.
    print(l1)
    print(l2)
    print("-------------")

    #The list at the position l1 is pointed to, gets to append 4. Not l1, but the list at that position.
    l1.append(4)
    print(l1)
    print(l2)
    print("-------------")
    print("-------------")
    #Since l2 is not the value itself, but a "name" that points to a position, print(l2) prints what l2 points to.
    #So since the list in that point of memory has changed, l2 seems to also have "changed".

def change_in_other_function():
    #String immutable example
    def change_str(s:str):
        s = s.lower()

    a = "Brent"
    change_str(a)
    print(a)
    #a hasn't changed, it just went to "change_str(s)" and did anything but change the value a.
    print("-------------")

    #List mutable example
    def change_list(lst:list):
        lst.append(4)
    l = [1, 2, 3]
    change_list(l)
    print(l)
    #List is mutable, so since l is just pointing to a place in memory, the value at the memory can be changed.
    print("-------------")
    print("-------------")

    def wrong_use_list_argument(lst: list = []):
        lst.append(4)

    wrong_use_list_argument(l)
    print(l)

    def wrong_use_list_argument(lst: list = None):
        if lst is None:
            lst = []

def main():
    ex_string_value_change()
    ex_list_value_change()
    change_in_other_function()

if __name__ == "__main__":
    main()