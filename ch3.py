def starredname(last_name, first_name):
    name  = last_name + " * " + first_name
    total_width = 40
    prefix = (total_width-(len(name)+2)) // 2
    postfix = (total_width-(len(name)+2)-prefix)
    prefix, postfix = postfix, prefix
    print(prefix*"*",name,postfix*"*")
    return

starredname("vorsselmans","robin")
starredname("vindevogel","yves")
print("*"*40)