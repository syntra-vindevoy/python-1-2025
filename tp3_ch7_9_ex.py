def uses_none(word, forbidden):
    """Checks whether a word avoid forbidden letters.

    >>> uses_none('banana', 'xyz')
    True
    >>> uses_none('apple', 'efg')
    False
    """
    for letter in forbidden.lower():
        if letter in word.lower():
            return False
    return True

def uses_only(word, available):
    """Checks whether a word uses only the available letters.

    >>> uses_only('banana', 'ban')
    True
    >>> uses_only('apple', 'apl')
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
    """
    for letter in required.lower():
        if letter not in word.lower():
            return False
    return True

def check_word(word, available, required):
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
    if required is not None or required is not "":
        assert required.lower() in available.lower()
        if required.lower() not in word.lower(): return False
    if len(word) < 4: return False

    #Option 1 (with external function)
    return uses_only(word, available)
    #Option 2 (manual code)
    # for letter in word.lower():
    #     if letter not in available.lower():
    #         return False
    # return True

def word_score(word, letters):
    """Compute the score for an acceptable word.

    >>> word_score('card', 'ACDLORT')
    1
    >>> word_score('color', 'ACDLORT')
    5
    >>> word_score('cartload', 'ACDLORT')
    15
    """
    if check_word(word, letters, ""):
        if len(word) == 4: return 1
        elif uses_all(word, letters): return len(word) + 7
        else: return len(word)
    return 0

def uses_all_using_only(word, required):
    """Checks whether a word uses all required letters.

    >>> uses_all_using_only('banana', 'ban')
    True
    >>> uses_all_using_only('apple', 'api')
    False
    """
    for letter in required.lower():
        if not uses_only(word, letter):
            return False
    return True