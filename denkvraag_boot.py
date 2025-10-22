def show_river():
    print("_"*40)
    print(f"Tijd: {tijd} minuten")
    print(links, end=" ")
    print("~"*20, end="")
    print(rechts)
    print(f"Boot staat {"links" if boot_links else "rechts"}")

def move_boat():
    global boot_links, tijd

    show_river()

    # Input en verifiëren ervan
    absent_choice = True
    a = None
    b = None
    while absent_choice:
        a = input("Persoon 1: ")
        if len(a) < 1: quit()
        a = int(a)

        b = input("Persoon 2: ")
        if len(b) > 0: b = int(b)
        else: b = None

        if a != b and a in (links if boot_links else rechts) and ((b is None) or b in (links if boot_links else rechts)): absent_choice = False
        else: print(f"Foute input, maak een unieke keuze uit {links if boot_links else rechts}")

    if boot_links:
        if a in links:
            links.remove(a)
            rechts.append(a)
        if b in links:
            links.remove(b)
            rechts.append(b)
    else:
        if a in rechts:
            rechts.remove(a)
            links.append(a)
        if b in rechts:
            rechts.remove(b)
            links.append(b)

    if b is not None: tijd += max(a, b)
    else: tijd += a
    boot_links = not boot_links
    if len(links) > 0: move_boat()
    return tijd

def main():
    move_boat()
    if 17 <= tijd: print("Perfect! ", end="")
    elif 17 > tijd <= 19: print("Goed gedaan, maar het kan beter! ", end="")
    elif 19 > tijd: print("Het kan beter ", end="")
    # Kijken of de tijd meer dan 19 is, is niet nodig, het staat er voor de duidelijkheid.
    print(f"Je bracht iedereen naar de andere kant in {tijd} minuten.")
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    links = [1,2,5,10]
    rechts = []
    boot_links = True
    tijd = 0

    main()