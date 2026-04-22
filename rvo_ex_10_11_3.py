from pathlib import Path

words = Path("words.txt").read_text().splitlines() #je moet geen with gebruiken om open en close the doen
""" this is useless better do it directly in the function longer_than
def has_duplicates(word) -> bool:
    if len(word)==len(set(word)):
        return False
    else:
        return True
"""
def longer_than(words):
    dict_to_return = {}
    for word in words:
        if len(word)<len('unpredictably'):
            continue
        if len(word)!=len(set(word)):
            continue
        else:
            if len(word)>len('unpredictably'):
                dict_to_return.update({word:word})
    return dict_to_return

def main():
    print(longer_than(words))

if __name__ == '__main__':
    main()



