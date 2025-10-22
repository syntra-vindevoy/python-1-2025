from datetime import datetime

def is_leapyear(year:int):
    if year % 400 == 0: return True
    if year % 100 == 0: return False
    return year % 4 == 0

def print_is_leapyear():
    print(is_leapyear(0))
    print(is_leapyear(1))
    print(is_leapyear(2))
    print(is_leapyear(3))
    print(is_leapyear(4))
    print("5")
    print(is_leapyear(5))
    print(is_leapyear(6))
    print(is_leapyear(7))
    print(is_leapyear(8))
    print(is_leapyear(9))
    print("10")
    print(is_leapyear(10))
    print(is_leapyear(11))
    print(is_leapyear(12))
    print(is_leapyear(13))
    print("100")
    print(is_leapyear(100))
    print(is_leapyear(104))
    print(is_leapyear(396))
    print(is_leapyear(400))
    print(is_leapyear(400))

def days_in_month(year:int, month:int):
    if month == 1 | month == 3 | month == 5 | month == 7 | month == 3 | month == 3: return 31
    if month == 2:
        if is_leapyear(year): return 29
        else: return 28
    return 30

def day_of_first_day_of_month(date:datetime):
    return datetime.date(date).replace(day=1)

def main():
    print("test")
    print(day_of_first_day_of_month(datetime(2021, 12, 28)))
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    main()