def starred_name(
    last_name: str, first_name: str, total_width: int = 60, char: str = "*"
):
    assert type(last_name) is str, "last_name must be a string"
    assert type(first_name) is str, "first_name must be a string"
    assert type(total_width) is int, "total_width must be a number"
    assert type(char) is str, "char must be a string"

    name = f"{last_name} {char} {first_name}"
    postfix = (total_width - 2 - len(name)) // 2
    prefix = total_width - 2 - len(name) - postfix

    print(char * prefix, name, char * postfix)


starred_name("Vindevogel", "Yves")
starred_name("Hendricx", "Brent", 40, "#")
starred_name("Marginet", "Christian", char="=")
starred_name(total_width=30, last_name="Van Acker", char="!", first_name="Femke")

print("*" * 40)

print(starred_name)
