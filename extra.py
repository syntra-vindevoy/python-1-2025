def validate_cardnumber(cardnumber: int) -> bool:
    number_part = cardnumber // 100
    # print("number_part = ", number_part)
    check_part = cardnumber % 100
    # print("check_part = ", check_part)

    return number_part % 97 == check_part

def main():
    assert validate_cardnumber(595084551177)

if __name__ == '__main__':
    main()
