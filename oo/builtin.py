
class XString(str):
  def mountainize(self):
        result = ""

        for i in range(len(self)):
            if i % 2 == 0:
                result += self[i].upper()
            else:
                result += self[i].lower()

        return XString(result)

x = XString("vindevogel")
x = x.mountainize()
print(x)
x = x.upper()