#from tp3_ch10_ex2 import letter_count

#count = letter_count('brontosaurus')
count = {}

print(count.items())
count = sorted(count.items(), key=lambda x: (-x[1], x[0]))
# Lambda functions saves your time.
# count = sorted(count.items(), key=lambda x: x[1], reverse=False)
# This sorts "count.items()" by the function x:x[1]. The 1 depicts the position of the tuple of dict, the second value.
# It sorts from 1 to positive infinity. BUT add - at "x:-x[1]" and it reverses that order. So you never need "reverse".
# Sorting on 2 values? Add them in order in brackets, like "x: (x[1], x[0])".
# The sorting on count needs to be sorted on "1" first, then "0". -> "x: (x[1], x[0])
# The letters in are sorted from a-z, but the numbers need to go from big to small -> reverse x[1] -> x: -x[1]
# So you get -> x: (-x[1], x[0])

print(count)

def toto(x: tuple[str, int]) -> int:
    return x[1]