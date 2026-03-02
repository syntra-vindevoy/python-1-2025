

class Toto:
    def __init__(self):
        from inherr import TotoValueError

        raise TotoValueError("Just a demo")

toto = Toto()