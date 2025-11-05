import math

# from tabulate import tabulate


def mysqrt(a, x):
    while True:
        y = (x + a / x) / 2
        if y == x:
            break
        x = y
    return y

def square_root():
    # print(tabulate(test))
    print("a", "mysqrt(a)", "math.sqrt(a)", "diff", sep="\t")
    print("-", "---------", "------------", "----", sep="\t")
    for i in range(1, 10, 1):
        x = mysqrt(i, i)
        y = math.sqrt(i)
        print(i, round(x, 10), round(y, 10), round(abs(x-y), 10), sep="\t")



def main():
    # square_root()
    # >> > eval('1 + 2 * 3')
    # 7
    # >> > import math
    # >> > eval('math.sqrt(5)')
    # 2.2360679774997898
    # >> > eval('type(math.pi)')
    # <
    #
    # class 'float'>
    #HIER PROGRAMMEREN
    print()

if __name__ == "__main__":
    main()