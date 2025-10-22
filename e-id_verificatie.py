def verify_e_id(eid:int):
    first_9 = eid // 100
    last_2 = eid % 100
    return first_9 % 97 == last_2

def main():
    print("test")
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    main()