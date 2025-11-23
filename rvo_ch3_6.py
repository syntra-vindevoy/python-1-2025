def delen(x: float, y: float) -> float:
    return x / y
def main():
    a = 4
    b = 0
    c = delen(a,b) #dit geeft een fout ZeroDivisionError - dit is geen semantic of syntax maar de derde error: runtime error

if __name__ == '__main__':
    main()