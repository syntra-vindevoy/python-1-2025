#V1) List first names (Met Yves als eerste) naam:classroom ; y=klinker
#V2) Remove all names starting with a vowel
#Wondelgem, turqua, zelzate, torhaut, gegaartsbergen, lede
from itertools import repeat


def wrong_way_to_take_out_things_in_list(): #Pop updates the list, with makes it so it skips the "next" item, that's been moved.
    classroom = ["Yves", "Brent", "Cristian", "Femke", "Uwe", "Yves"]

    for name in classroom:
        if name[0].upper() in "AEIOUY":
            #         classroom.remove(name)    #De remove loopt over de lijst, nog eens, per keer de if true is
            classroom.pop(classroom.index(name))
            #   The pop delete deletes an entry, the list is edited, but the supposed next item is skipped since
            #   it took the place of the deleted item. The for does +1 to the iteration.
            #   So, since the list moves all items once to the left, and the for once to the right, you get a hop of 2.
            print(classroom)

    print(classroom)