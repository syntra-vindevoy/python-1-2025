

def fac(n):
  def go(n, a):

    while n > 0:
        a = n * a
        n = n - 1

    return a

  return go(n, 1)

def fibo(n):
    def go(n, a, b):
        while n > 0:
            c = a
            a = b
            b = c + a
            n = n - 1

        return a

    return go(n, 0, 1)

def main():
    print(fibo(1000))

if __name__ == '__main__':
    main()


