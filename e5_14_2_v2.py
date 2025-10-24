def check_fermat(a, b, c, n):
    if a<=0 or b<=0 or c<=0:
        return "a,b,c must be positive non-zero integers"
    if n == 0 or n==1 or n==2:
        return "n must be greater than 2"
    apower = a**n
    bpower = b**n
    cpower = c**n
    if (apower+bpower)==cpower:
        return "Holy smokes, Fermat was wrong!"
    else:
        return "no that doesn't work"
def user_input_fermat():
    a = int(input("enter a: "))
    b = int(input("enter b: "))
    c = int(input("enter c: "))
    n = int(input("enter n: "))
    return check_fermat(a, b, c, n)

def main():
    check = user_input_fermat()
    print(check)

if __name__ == '__main__':
    main()