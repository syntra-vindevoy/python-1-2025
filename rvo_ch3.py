def starredname(
    last_name: str, first_name: str, char: str = "*", total_width: int = 60
):
    assert type(last_name) is str, "last_name must be str"
    assert type(first_name) is str, "first_name must be str"
    assert type(char) is str, "char must be str"
    assert type(total_width) is int, "total_width must be int"

    name = last_name + f" {char} " + first_name
    prefix = (total_width - (len(name) + 2)) // 2
    postfix = total_width - (len(name) + 2) - prefix
    prefix, postfix = postfix, prefix
    print(prefix * char, name, postfix * char)
    return


starredname("vorsselmans", "robin", "#", 40)
starredname("vindevogel", "yves", char="_")
# starredname(10,10,10,10)
print("*" * 60)
