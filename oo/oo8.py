from datetime import date

class Person:
    @classmethod
    def __init__(self, first_name: str, last_name: str, birthday: date, is_alive: bool = True):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.is_alive = True
        # __ puts the property as a private accessible property only usable inside the class.
        self.__nationality = "Belgian"

    @property   # Used for declaring the function without the need of brackets ().
    def age(self):
        today = date.today()

        years = today.year - self.birthday.year

        #subtract 1 if birthday
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            years -= 1

        return years

    @property
    def is_belgian(self):
        return self.__nationality == "Belgian"


def main():
    p = Person(first_name="John", last_name="Doe", birthday=date(1972,12,31))
    print(p.first_name)
    print(p.last_name)
    print(p.birthday)
    print(p.age)
    print(p._Person__Nationality)

    print(p.__dict__)

if __name__ == '__main__':
    main()