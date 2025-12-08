"""
Een lijst met alle getal van 1 tot en met 10.000.
Uw programma maakt een random int.
Maak een binaire search.
De search moet het random getal zoeken.
Het gokt, correct? Het wint. Is het fout? dan:
De search zegt of het getal dat is gegokt groter of kleiner,
	en zoekt dan verder met de nieuwe limieten.

Doe het vaak, en onthou het MAXIMUM je het aantal keren een keer moest doen om het te vinden.
"""

def search_this_number(num:int, min:int, max:int):
    guess = num
    guess = guess/2
    if guess < num:
        return search_this_number(num, round(guess/2), max)
    elif guess > num:
        return search_this_number(num, min, round(guess/2))
    elif guess == num:
        return guess
    return -1



def main():
    search_this_number(1, 0, 20)

if __name__ == "__main__":
    main()