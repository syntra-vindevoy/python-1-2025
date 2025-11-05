def calc_stone_weights():
    avail_stones = [1, 3, 9, 27]
    used_stones = []

    def inputs():
        print(f"Stenen gebruikt: {used_stones}")
        print(f"Kies uit {avail_stones}")
        stones = []
        while len(avail_stones) > 0:
            try:
                a = input("stone: ")
                if a == "": break
                a = int(a)
                if a not in avail_stones or a in used_stones: raise ValueError()

                avail_stones.remove(a)
                used_stones.append(a)
                stones.append(a)

            except ValueError:
                print(f"Foute input, maak een unieke keuze uit {avail_stones}")
        return stones

    links = inputs()
    rechts = inputs()
    print(f"{links} | {rechts}")

    while True:
        operator = input("- of +    ")
        if operator == "-":
            return f"U heeft {0+sum(links) - 0+sum(rechts)} berekend."
        elif operator == "+":
            return f"U heeft {0+sum(links) + 0+sum(rechts)} berekend."
        elif operator == "":
            exit()
        else:
            print("Geef een geldige operator mee.")


def main():
    while True:
        print(calc_stone_weights())

if __name__ == "__main__":
    main()