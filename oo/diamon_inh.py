

class A:
    def __init__(self, a, *args, **kwargs):
        print("Entering A")

        super().__init__(*args, **kwargs)

        print("a becomes", a)
        self.a = a

        print("Exiting A")

class B:
    def __init__(self, b, *args, **kwargs):
        print("Entering B")

        super().__init__(*args, **kwargs)

        print("b becomes", b)
        self.b = b

        print("Exiting B")

class C(A, B):
    def __init__(self, *args, **kwargs):
        print("Entering C")

        super().__init__(*args, **kwargs)

        print("Exiting C")

print(C.mro())
c = C(a=1, b=2)



