from datetime import date


class Person:
    def __init__(
        self, *, first_name: str, last_name: str, birthdate: date, is_alive: bool = True
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.is_alive = is_alive

        self.__nationality = "Belgian"

    @property
    def age(self):
        today = date.today()

        years = today.year - self.birthdate.year

        # Subtract 1 if birthday hasn't occurred yet this year
        if (today.month, today.day) < (self.birthdate.month, self.birthdate.day):
            years -= 1

        return years


    @property
    def is_belgian(self):
        return self.__nationality == "Belgian"

p = Person(first_name="Yves", last_name="Vindevogel", birthdate=date(1972,12,31))

p.first_name = "Jacques"

print(p.is_belgian)

print(p.last_name)
print(p.age)


