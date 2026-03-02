class A:
    def __init__(self):
        print("A")

class B:
    def __init__(self):
        super().__init__() # Do what in the __init__ is of the super/inherited.
        print("B")

class C:
    def __init__(self):
        super().__init__() # Do what in the __init__ is of the super/inherited.
        print("C")

def main():
    C()
    # Init C -> super.init -> Init B -> super.init -> init A
    #   -> print("A") -> init A done
    #   -> print("B") -> init B done
    #   -> print("C")

if __name__ == '__main__':
    main()