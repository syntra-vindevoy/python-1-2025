from oo.basket import Basket
from oo.orange import Orange

def main():
    pass

if __name__ == "__main__":
    b = Basket()
    o = Orange()

    b.put_in_basket(o)
    print(b.content)

# Notes
#
# from oo.orange import Orange
# from oo.basket import Basket
# Circular reference: Basket imports Orange, Orange imports Basket, ... -> endless loop
#
# Polymorphisme = alles van onderliggende klasse implementeren
#   Het kennen maar het bestaat niet in Python, je kan enkel gebruik maken van overerving.