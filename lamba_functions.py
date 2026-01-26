from ex10_11_2 import letter_count

count = letter_count('brontosaurus')

print(count.items())
count = sorted(count.items(), key=lambda x: (-x[1], x[0]), reverse=False)

print(count)


def toto(x: tuple[str, int]) -> int:
    return x[1]