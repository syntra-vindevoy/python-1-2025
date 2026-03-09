lang = "EN"

class OUT:
    def save(self, o: O):
        raise NotImplementedError("You forgot save")

class EN(OUT):
    def __init__(self):
        pass

    def save(self, o: O):
        print(f"{type(o).__name__} is saved as", o)

class NL(OUT):
    def __init__(self):
        pass

    def save(self, o: O):
        print(f"{self.__class__.__name__} is bewaard als", o)

class O:
    def __init__(self, outputter: OUT):
        self.outputter = outputter

    def save(self):
        self.outputter.save(self)

class A(O):
    def __init__(self, a, outputter):
        super().__init__(outputter)

        self.a = a

    def __str__(self):
        return f"A({self.a})"


class B(O):
    def __init__(self, b, outputter):
        super().__init__(outputter)

        self.b = b

    def __str__(self):
        return f"B({self.b})"

langs = {"EN": EN(), "NL": NL()}

if lang not in langs:
    raise Exception(f"No such language: {lang}")

outputter = langs[lang]

a1 = A(1, outputter)
a2 = A(2, outputter)
b1 = B(1, outputter)

a1.save()
b1.save()

