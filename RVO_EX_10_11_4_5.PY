def find_repeats(counter:str):
    tracker = {}
    if len(counter)==len(set(counter)):
        return []
    else:
        for char in counter:
            if tracker.get(char,0)==0:
                tracker.update({char:1})
            elif tracker.get(char,0)==1:
                tracker[char]+=1
    tracker = {char: tracker[char] for char in tracker if tracker[char] > 1}
    return list(tracker.keys())

def value_counts(counter: str):
    tracker = {}
    for char in counter:
        tracker[char] = tracker.get(char, 0) + 1
    return tracker


def add_counters(counter1:dict, counter2:dict):
    tracker = counter1.copy()
    for char, count in counter2.items():
        tracker[char] = tracker.get(char, 0) + count #
    return tracker

def letter_count2(word:str):
    return {letter:word.count(letter) for letter in word} #gaat wel dubbel over

def main():
    #counter = 'brontosaurus'
    counter = 'apatosaurus'
    print(find_repeats(counter))
    counter1 = value_counts('brontosaurus')
    counter2 = value_counts('apatosaurus')
    counter3 = add_counters(counter1,counter2)
    print(counter1)
    print(counter2)
    print(counter3)
    count = sorted(counter3.items(), key=lambda x: (-x[1], x[0]), reverse = False) #die - zorgt ervoor dat ze van hoog naar laag gesorteerd worden
    print(count)


if __name__ == '__main__':
    main()

