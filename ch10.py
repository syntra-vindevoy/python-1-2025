client = {}

client["name"] = "Syntra"
client["orders"] = [1, 5, 98]
client["address"] = ["The street"]

clients = dict()

clients["cus0001"] = client

print(clients["cus0001"])

supplier = {"name": "Microsoft", "address": "Redmond"}

print(clients["cus0001"]["name"])

clients["cus0001"]["birth_date"] = "1972-12-31"

print(clients["cus0001"])

print(client)

if "toto" in clients:
    t = clients["toto"]


t = clients.get("toto", "Unknown")

print(len(clients))
print(len(client))

supplier = {"a": 1, "b": 2, "c": 3}
supplier["a"] = 4

toto = {"a": 1, "b": 2, "c": 3}
tata = {"a": 1, "b": 2, "c": 3}

print(toto == tata)
print(toto is tata)

toto["a"] = 4
print(tata)

titi = toto
toto["b"] = 5
print(titi)

tutu = toto.copy()

if "a" in tutu:
    pass

if "b" in tutu:
    pass

if "c" in tutu.keys():
    pass

if 2 in tutu.values():
    pass

word_list = open('words.txt').read().split()

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

def one_liner():
    d = {word:1 for word in word_list}
    c = sum(list({d[k] for k in d.keys() if k[::-1] in d}))
    return d

print(one_liner())


