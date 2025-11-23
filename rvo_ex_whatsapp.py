def check_eid(eid):
    from datetime import datetime
    birthyear = eid//1000000000
    current_year_full = datetime.today().year
    current_year_short = current_year_full%100
    check_num = eid %100
    short_eid = eid//100
    if birthyear <= current_year_short: #dit loopt fout als iemand ouder is dan 100?
        short_eid = short_eid + (2*1000000000)
    check_contra = 97-(short_eid%97)
    if check_num == check_contra:
        print("This is a valid EID")
    else:
        print("This is NOT a valid EID")

def check_card_number(card_number):
    check_digits = card_number % 100
    number_without_check = card_number // 100
    mod_result = number_without_check % 97
    valid1 = (mod_result == check_digits)
    valid2 = ((100 - mod_result) == check_digits)

    if valid1 or valid2:
        print("Dit is een geldig eID kaartnummer")
    else:
        print("Dit is GEEN geldig eID kaartnummer")

def male_or_female(eid):
    number_without_check = eid // 100
    identifier = number_without_check % 1000
    if (identifier%2)==1:
        print("This person is born male")
    elif (identifier%2)==0:
        print("This person is born female")
    else:
        print("An unexpected error occured")

def leap_year(year):
    if (((year % 4) == 0) and (year % 100 != 0)) or (year%400 == 0):
        return True
    else:
        return False

def is_leapyear_yves(year: int)->bool:
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0

def days_in_month(year, month):
    assert type(year) == int, "Year must be an integer"
    assert type(month) == int, "Month must be an integer"
    assert 0<month and month<13, "input must be between 1 and 12"
    if month in [1,3,5,7,8,10,12]:
        return 31
    elif month in [4,6,9,11]:
        return 30
    elif month ==2:
        if leap_year(year)==True:
            return 29
        else:
            return 28

def dom_yves(year:int, month:int)->int:
    assert type(year) == int, "Year must be an integer"
    assert type(month) == int, "Month must be an integer"
    assert 0<month and month<13, "input must be between 1 and 12"
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        return 31
    if month == 2: #je kan ook return 28+is_leapyear(year) -> geeft 1 als het een schrikkeljaar is.
        if is_leapyear_yves(year):
            return 29
        else:
            return 28
    return 30

def dom2(y:int,m:int)->int:
    assert type(y) == int, "Year must be an integer"
    assert type(m) == int, "Month must be an integer"
    assert 0<m and m<13, "input must be between 1 and 12"
    return [31,28+is_leapyear_yves(y),31,30,31,30,31,31,30,31,30,31][m-1]

def day_of_week(y, m, d):
    t = [0, 3, 2, 5, 0, 3, 5, 1, 4, 6, 2, 4]
    if m < 3:
        y -= 1
    return (y + y//4 - y//100 + y//400 + t[m-1] + d) % 7

def first_day_of_month(jaar, maand):
    daylist = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    nummer = day_of_week(jaar,maand,1)
    return daylist[nummer]

def prime(t):
    if t <= 1:
        return False
    for i in range(2,t):
        if t % i == 0:
            return False
    return True

def is_prime(n):
    assert type(n) is int, "must be int"
    assert n>0, "n must be positive"

    if n<=2:
        return True #niet persé waar want één is in principe geen priemgetal

    if n%2 == 0:
        return False
    for i in range (3, n**0,5+1,2):
        if n % i == 0:
            return False
    return True

def main():
    eid_nummer = 92041612792
    kaartnummer = 595423133115
    jaar = 1992
    check_eid(eid_nummer)
    check_card_number(kaartnummer)
    male_or_female(eid_nummer)
    if leap_year(jaar) == True:
        print(str(jaar)+" is een schrikkeljaar")
    else:
        print(str(jaar)+" is geen schrikkeljaar")
    print(days_in_month(jaar, 2))
    print(first_day_of_month(jaar, 2))
    prime_check = 19
    if prime(prime_check)==True:
        print(str(prime_check)+" is a prime number")
    else:
        print(str(prime_check)+" is not a prime number")
    #print(is_leapyear_yves(None))
    print(dom2(1992, 3))
    print(day_of_week(1992, 4, 16))


if __name__ == '__main__':
    main()
