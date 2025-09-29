max_char = 40
char = '#'
text = "brent"

def line_with_stars(text):
    padding = (len(text) + 1) // 2
    return f"{char * padding} {text} {char * padding}"

print(line_with_stars(text))