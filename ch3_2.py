import math # Om math.pi te kunnen gebruiken.
import datetime

def rounded_pi(n):      # Nooit een functie combineren met een manier om het om te vormen met text of print in gebruiken
    return round(math.pi, n)    # Als je meer en meer functies moet schrijven om de bovenstaande regel te volgen, is het dan zo.
def factorial_recursive(n): # Kan errors krijgen als getal te hoog is (vanaf 6 en hoger) #line repeated 995 more times   RecursionError: maximum recursion depth exceeded
    if n == 0:
        return 1
    else:
        return n * factorial_recursive(n - 1)
def factorial(n):
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

start_ts = datetime.datetime.now()
for i in range(10000):
    factorial_recursive(500)
end_ts = datetime.datetime.now()
print(f"Time taken with factorial recursive functions: {end_ts - start_ts}")

start_ts = datetime.datetime.now()
for i in range(10000):
    factorial(500)
end_ts = datetime.datetime.now()
print(f"Time taken with factorial using 'for': {end_ts - start_ts}")

def main():
    assert factorial(1) == 1, "factorial(3) must be 1"
    assert factorial(3) == 6, "factorial(3) must be 6"
    assert factorial(4) == 24, "factorial(3) must be 24"
#    print(factorial(1000))  #line repeated 995 more times   RecursionError: maximum recursion depth exceeded
    x = factorial(5)
    print(x)

if __name__ == "__main__":
    main()