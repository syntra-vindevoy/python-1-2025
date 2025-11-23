" bewijs dat je alles kan maken 1,3,9,27, brug raadsel"

def stone_question(x, stones=[27, 9, 3, 1]):
    if x == 0:
        return ""
    if not stones:
        return None

    current = stones[0]
    rest = stones[1:]

    result = stone_question(x - current, rest)
    if result is not None:
        return f"+{current} " + result

    result = stone_question(x + current, rest)
    if result is not None:
        return f"-{current} " + result

    return stone_question(x, rest)



print(stone_question(40))



