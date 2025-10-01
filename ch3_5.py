def say_hello(who: str):
    name = "Brent"

    print(f"Hello, {who}!")

def main():                     # Standaard in elke code te zetten om "shadow names" te vermijden  (Gebruik met [if __name__ == "__main__":]    main())
    name = "Yves"

    say_hello(name)

    print("name:", name)

if __name__ == "__main__":      # Standaard in elke code te zetten om "shadow names" te vermijden (Gebruik met [def main():])
    name = "Brent"  # Gebruikt als voorbeeld. Is nu gedeclareerd als "globale variabel"
    main()  # Eens deze functie compleet is, gaan de variabelen en hun waarde erin kwijt zijn. Name hierna is terug "Brent".
    print("name:", name)