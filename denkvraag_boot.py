def show_river():
    print("_"*40)
    print(f"Tijd: {TIME} minuten")
    print(LEFT, end=" ")
    print("~"*20, end="")
    print(RIGHT)
    print(f"Boot staat {"links" if BOAT_LEFT_SIDE else "rechts"}")

def move_boat(a, b):
    global BOAT_LEFT_SIDE, TIME

    if BOAT_LEFT_SIDE:
        if a in LEFT:
            LEFT.remove(a)
            RIGHT.append(a)
        if b in LEFT:
            LEFT.remove(b)
            RIGHT.append(b)
    else:
        if a in RIGHT:
            RIGHT.remove(a)
            LEFT.append(a)
        if b in RIGHT:
            RIGHT.remove(b)
            LEFT.append(b)

    if b is not None: TIME += max(a, b)
    else: TIME += a
    BOAT_LEFT_SIDE = not BOAT_LEFT_SIDE
    if len(LEFT) > 0: move_boat(a, b)
    return TIME

def user_moves_boat(passengers:list[int]):
    global LEFT
    LEFT = passengers

    show_river()
    while len(LEFT) > 0:
    # Input en het verifiëren ervan
        while True:
            try:
                a = int(input("Persoon 1: "))
                if a not in (LEFT if BOAT_LEFT_SIDE else RIGHT): raise ValueError()

                b = input("Persoon 2: ")
                if len(b) > 0:
                    b = int(b)   # Geeft ValueError las het letters zijn, als er niets in staat ook
                    if b not in (LEFT if BOAT_LEFT_SIDE else RIGHT): raise ValueError()
                else: b = None

                if a != b: break
                else: raise ValueError()

            except ValueError:
                print(f"Foute input, maak een unieke keuze uit {LEFT if BOAT_LEFT_SIDE else RIGHT}")

        if len(LEFT) > 0: move_boat(a, b)

    if 17 >= TIME: print("Perfect! ", end="")
    elif 17 < TIME <= 19: print("Goed gedaan, maar het kan beter! ", end="")
    else: print("Het kan beter ", end="")
    print(f"Je bracht iedereen naar de andere kant in {TIME} minuten.")

def solve_boat(passengers:list[int]):
    global LEFT
    LEFT = passengers
    while len(LEFT) > 0:
        for i in range(len(LEFT)):
            for j in range(len(LEFT)-1):
                LEFT = passengers
                move_boat(i, j)

def main():
    solve_boat([1, 2, 5, 10])
    #user_moves_boat([1, 2, 5, 10])
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    LEFT = []
    RIGHT = []
    BOAT_LEFT_SIDE = True
    TIME = 0

    main()