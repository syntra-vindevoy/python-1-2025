from pathlib import Path

def is_interlocking(word, valid_words):
    part1 = word[0:2]
    part2 = word[1:2]

    return part1 in valid_words and part2 in valid_words[part1], word, part1, part2

def main():
    words = Path("words.txt").read_text().split("\n")
    valid_words = {word: True for word in words if len(word) > 3}

    for word in valid_words:
        if len(word) < 8:
            continue

        interlocks, word, part1, part2 = is_interlocking(word, valid_words)


if __name__ == "__main__":
    main()