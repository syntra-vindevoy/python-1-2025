class XString(str):
    def __init__(self, s:str):
        super().__init__(s)

    def mountainize(self):
        result = ""

        for i in range(len(self)):
            if i % 2 == 0:
                result += self[i].upper()
            else:
                result += self[i].lower()

        return XString(result)
    