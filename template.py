def say_hello(*who: str):
    print(f"Hello, {who}!")

def main():                 # Standaard in elke code te zetten om "shadow names" te vermijden  (Gebruik met [if __name__ == "__main__":]    main())
    name = "Brent"
    say_hello(name)
if __name__ == "__main__":  # Standaard in elke code te zetten om "shadow names" te vermijden (Gebruik met [def main():])
    main()