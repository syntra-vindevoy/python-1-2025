class TotoValueError(ValueError):
    print(f"Error: {ValueError}")
    pass

def divide(x: int, y: int) -> float:
    result:float = 0
    if y == 0:
        raise TotoValueError("y cannot be 0")
    return result

def main():
    divide(1,0)

if __name__ == "__main__":
    main()