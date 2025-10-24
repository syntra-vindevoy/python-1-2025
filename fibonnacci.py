def fibonacci(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else:
        return fibonacci(n-1)+fibonacci(n-2)

def fibonacci_tail(n):
    def go(i, a, b):
        if i == 0:
            return a
        return go(i - 1, b, a + b)
    return go(n, 0, 1)


def fibonacci_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def main():
    #print(fibonacci(10))
    #print(fibonacci_tail(10))
    print(fibonacci_iter(1000))
if __name__=="__main__":
    main()