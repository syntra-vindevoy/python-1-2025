class XString(str):
    def __new__(cls, s: str):
        return super().__new__(cls, s)

    def mountainize(self):
        result = ""

        for i in range(len(self)):
            if i % 2 == 0:
                result += self[i].upper()
            else:
                result += self[i].lower()

        return XString(result)


x = XString("Robin")
x = x.mountainize()
print(x)

#flet
#NiceGUI - web
#wxpython - enkel desktop
#rio - webapp
#buridan ui
#panel
#streamlet -- niet zo goed volgens yves
#dash
#shiny for python - geemaakt voor statistiek
#altair viz - best in een wrapper steken of in eigen class