def verify_e_id(eid:int):
    first_9 = eid // 100
    last_2 = eid % 100
    return first_9 % 97 == last_2

def eid_verification(eid: str) -> bool: #Using chatgpt
    """
    Validate a Belgian National Register number (11 digits + optional separators).
    Format: YYMMDDXXXCC
    """

    # Remove common separators (., -, space)
    cleaned = ''.join(ch for ch in eid if ch.isdigit())

    if len(cleaned) != 11:
        return False

    first9 = cleaned[:9]
    checksum = int(cleaned[9:11])

    # Birth year indicator: determines if "2" prefix is used for post-2000 births
    # Try pre-2000 formula
    try_pre2000 = 97 - (int(first9) % 97)
    if try_pre2000 == checksum:
        return True

    # Try post-2000 formula
    try_post2000 = 97 - (int("2" + first9) % 97)
    if try_post2000 == checksum:
        return True

    return False


    # Example usage:
    samples = [
        "97.07.15-123.61",   # valid example (born 1997)
        "03.01.20-456.82",   # valid example (born 2003)
        "99010112345",       # invalid
    ]

    for s in samples:
        print(f"{s}: {'VALID' if eid_verification(s) else 'INVALID'}")

def main():
    print("test")
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    main()