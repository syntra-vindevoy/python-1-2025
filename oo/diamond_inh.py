

class A:
    def __init__(self):
        print("Entering A")
        print("Exiting A")
class B:
    def __init__(self):
        print("Entering B")
        print("Exiting B")
class C (A,B):
    def __init__(self):
        print("Entering C")

        #super(A, self).__init__(self) # Ent C, ent A, exit A, exit C.      When inheriting from A and B. Only first super innit.

        A.__init__(self)    # Solution to question of calling 2 super.innit from the 2 inherited classes.
        B.__init__(self)

        print("Exiting C")

def main():
    print(C.mro())  # MRO = Methode Resolution Order.

    c = C()


if __name__ == "__main__":
    main()