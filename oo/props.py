from datetime import date


class Person:
    name: str = ""
    date_of_birth: date = None

    @property
    def age(self) -> int:
        return (date.today() - self.date_of_birth).days // 365


yves = Person()
yves.name = "Yves"
yves.date_of_birth = date(1972, 12, 31)

print(yves.age)
