from oo.apple import Apple
from oo.basket import Basket
from oo.orange import Orange
#circular referencing is a nono en mag dus niet

def main():
    pass

if __name__ == '__main__':
    b = Basket()
    o = Orange()

    b.put_in_basket(o)

""" docstrings schrijven op classes en je kan ook docstrings schrijven op methods sfinx autoclass"""