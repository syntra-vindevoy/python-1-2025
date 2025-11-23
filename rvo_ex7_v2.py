import math

def mysqrt(a):
    x=3
    while True:

        y = (x + a / x) / 2
        if y == x:
            return y
        x = y

def run_test_square_root():
    print('a'+(3*' ')+'mysqrt(a)'+(5*' ')+'math.sqrt(a)'+(2*' ')+'diff')
    print('-'+(3*' ')+(9*'-')+(5*' ')+('-'*12)+(2*' ')+(4*"-"))
    for i in range(1,10,1):
        a = i
        result1 = mysqrt(a)
        result2 = math.sqrt(a)
        diff = abs(result1 - result2)
        printresult1 = round(result1, 11)
        printresult1 = str(printresult1)
        length = len(printresult1)
        if 0 < length < 13:
            printresult1 = printresult1+((13-length)*'0')
        printresult2 = round(result2, 11)
        printresult2 = str(printresult2)
        length = len(printresult2)
        if 0 < length < 13:
            printresult2 = printresult2+((13-length)*'0')
        a = round(float(a),1)
        print(str(a)+' '+printresult1+' '+printresult2+' '+str(diff))

def eval_loop():
    x = None
    while x != "done":
        x = input("Write something to evaluate, if you want to quit write done:")
        y = eval(x)
        print(str(y))
    print(str(y))

def eval_loop2():
    x = ""
    y = None
    while x != "done":
        x = input("Write something to evaluate, if you want to quit write done: ")

        if x == "done":
            break

        try:
            y = eval(x)
            print(y)
        except Exception as e:
            print(f"Error: {e}")

    # prints last evaluated value (if any)
    if y is not None:
        print(y)


def estimate_pi():
    total = 0
    y = 0
    term = 1  #make sure u don't get thrown out before iteration

    while term > 1e-15:
        term = (math.factorial(4 * y) * (1103 + 26390 * y)) / ((math.factorial(y) ** 4) * (396 ** (4 * y)))
        total += term
        y += 1

    factor = (2 * math.sqrt(2)) / 9801
    return 1 / (factor * total)


def main():
    #mysqrt(4)
    #run_test_square_root()
    #eval_loop() werkt niet goed
    #eval_loop2()
    check = estimate_pi()
    check2 = math.pi
    diff = abs(check - check2)
    print(check)
    print(check2)
    print(diff)

if __name__ == "__main__":
    main()