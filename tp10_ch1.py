def dictionary_examples():
    client = {} #Dict is een mutable zoals een list
    client["name"] = "Syntra"
    client["orders"] = [1, 5, 98]

    clients = dict()

    clients["cl00001"] = client

    print(clients)
    print(clients["cl00001"])

    supplier = {"name": "Supplier", "address": "Home"}

    print(clients["cl00001"]["name"])

    if "toto" in clients:
        t = clients["toto"]

    print(len(clients))
    print(len(client))

    supplier = {"a": 1, "b": 2, "c": 3}
    supplier["a"] = 4 #It changes the value at a, and doesn't add one behind. Keys are UNIQUE.

    toto = {"a": 1, "b": 2, "c": 3}
    tata = {"a": 1, "b": 2, "c": 3}
    toto["a"] = 4
    print(tata) #Different dictionaries are different and Unique

    print(toto == tata) #True, the values and keys are the same.
    print(toto is tata) #False, the two dictionaries DO NOT point to the same values in memory.

    titi = toto
    titi["a"] = 5
    print(toto) #Titi has been changed, but toto too. Since titi = toto, it pointed titi to the same place toto points to.

    tutu = toto.copy()

    if "a" in tutu:
        pass

    if "b" in tutu:
        pass

    if "c" in tutu.keys():
        pass

    if 2 in tutu.values():  #Traag
        pass


word_list = open('words.txt').read().split()
len(word_list)
def reverse_word(word):
    return ''.join(reversed(word))

def too_slow():
    count = 0
    for word in word_list:
        if reverse_word(word) in word_list:
            count += 1
    return count

def not_slow():
    d = {}
    count = 0

    for word in word_list:
        if word[::-1] in d:
            count += 1
        else:
            d[word] = word

    return count

def not_slow_two_line():
    d = {word:1 for word in word_list}
    c = sum(list({d[k] for k in d.keys() if k[::-1] in d}))

    return c

print(not_slow_two_line())