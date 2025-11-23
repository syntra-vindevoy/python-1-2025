def is_between(x:int,y:int,z:int) -> bool:
    assert type(x) == int and type(y) == int and type(z) == int, "all must be integer"
    if (x < y < z) or (z < y < x):
        return True
    else:
        return False

def ackermann(m:int,n:int):
    assert type(m) == int and type(n) == int, "all must be integer"
    if m == 0:
        return n+1
    elif (m>0) and (n==0):
        return ackermann(m-1,1)
    elif m>0 and n>0:
        return ackermann(m-1,ackermann(m,n-1))

def GCD(a:int,b:int):
    if b==0:
        return a
    else:
        return GCD(b,a%b)


def main():
    print(is_between(20,10,2))
    print(ackermann(2,10))
    print(GCD(45,135))

if __name__ == '__main__':
    main()