""" 7,9,1 - the else in the loop will stop the function after the first check"""
""" N-queens, blijkbaar is het mogelijk om 8 koningingen op een bord van 8 op 8 te zetten zonder dat een de andere kan slaan"""
from doctest import run_docstring_examples
def uses_none(word:str,forbidden:str):
    """Checks whether a word avoid forbidden letters.

    >>> uses_none('banana', 'xyz')
    True
    >>> uses_none('apple', 'efg')
    False
    >>> uses_none('banana', 'efg')
    True
    """
    for letter in word.lower():
        if letter in forbidden:
            return False
    return True


def uses_only(word, available):
    """Checks whether all letters in 'available' are in 'word'.

    >>> uses_only('banana', 'ban')
    True
    >>> uses_only('apple', 'apl')
    False
    >>> uses_only('apple', 'aplz')
    False
    """
    for letter in word.lower():
        if letter not in available.lower():
            return False
    return True


def uses_all(word, required):
    """Checks whether a word uses all required letters.

    >>> uses_all('banana', 'ban')
    True
    >>> uses_all('apple', 'api')
    False
    >>> uses_all('pear','xyz')
    False
    """
    for letter in required.lower():
        if letter not in word.lower():
            return False
    return True


def check_word(word, available, required = None):
    """Check whether a word is acceptable.

    >>> check_word('color', 'ACDLORT', 'R')
    True
    >>> check_word('ratatat', 'ACDLORT', 'R')
    True
    >>> check_word('rat', 'ACDLORT', 'R')
    False
    >>> check_word('told', 'ACDLORT', 'R')
    False
    >>> check_word('bee', 'ACDLORT', 'R')
    False
    """

    if len(word) < 4:
        return False
    if required.lower() not in word.lower():
        return False
    for letter in word.lower():
        if letter not in available.lower():
            return False
    return True
""" dit is fout en werkt niet naar behoren
def word_score(word, available):
    Compute the score for an acceptable word.

    >>> word_score('card', 'ACDLORT')
    1
    >>> word_score('color', 'ACDLORT')
    5
    >>> word_score('cartload', 'ACDLORT')
    15
    
    if len(word) ==4:
        return 1
    for letter in available.lower():
        if letter not in word.lower():
            break
    else:
        return 15
    return len(word)
"""
def uses_all2(word, required):
    """Checks whether a word uses all required letters.

        >>> uses_all('banana', 'ban')
        True
        >>> uses_all('apple', 'api')
        False
        >>> uses_all('pear','xyz')
        False
        """
    return uses_only(required, word)

def mysqrt(a):
    x=a-1
    while True:
        print(x)
        y = (x + a / x) / 2
        if y == x:
            break
        x = y

def word_score2(word, letters):
    """
    >> > word_score('card', 'ACDLORT')
    1
    >> > word_score('color', 'ACDLORT')
    5
    >> > word_score('cartload', 'ACDLORT')
    15
    """
    for w in word:
        if w not in letters:
            return 0
    extrapoints = 7
    for letter in letters:
        if letter not in word.lower():
            extrapoints = 0
            break
    if len(word) == 4:
        return 1
    return len(word)+extrapoints



def run_doctests(func):
    run_docstring_examples(func, globals(), name=func.__name__)

def main():
    run_doctests(uses_none)
    run_doctests(uses_only)
    run_doctests(uses_all2)
    run_doctests(check_word)
    run_doctests(word_score2)
    mysqrt(4)

if __name__ == "__main__":
    main()
