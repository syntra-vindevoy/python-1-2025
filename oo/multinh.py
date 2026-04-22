class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        print("B")

class C(B):
    def __init__(self):
        print("C")
c = C()

class A:
    def __init__(self):
        print("A")

class B(A):
    def __init__(self):
        super().__init__()
        print("B")

class C(B):
    def __init__(self):
        super().__init__()
        print("C")

c = C()

#dit is multiple inheritance, komt redelijk veel voor tot 4 a 5 niveaus