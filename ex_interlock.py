def interlock(word1, word2):
    return "".join(["".join(item) for item in zip(list(word1), list(word2), strict=False)])


print(interlock("shoe", "cold"))