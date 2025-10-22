from numpy.f2py.auxfuncs import throw_error


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
    while True:
        try:
            a = int(input("Persoon 1: "))
            if a not in (links if boot_links else rechts): raise ValueError()

            b = input("Persoon 2: ")
            if len(b) > 0:
                b = int(b)   # Geeft ValueError las het letters zijn, als er niets in staat ook
                if b not in (links if boot_links else rechts): raise ValueError()
            else: b = None

            if a != b: break
            else: raise ValueError()

        except ValueError:
            print(f"Foute input, maak een unieke keuze uit {links if boot_links else rechts}")

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
    else: print("Het kan beter ", end="")
    print(f"Je bracht iedereen naar de andere kant in {tijd} minuten.")
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    links = [1,2,5,10]
    rechts = []
    boot_links = True
    tijd = 0

    main()