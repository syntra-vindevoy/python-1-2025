import numpy as np
def create_bingo_card():
    column_1 = np.random.choice(np.arange(1,16),size=5,replace=False)
    column_2 = np.random.choice(np.arange(16,31),size=5,replace=False)
    column_3 = np.random.choice(np.arange(31,46),size=5,replace=False)
    column_4 = np.random.choice(np.arange(46, 61),size=5,replace=False)
    column_5 = np.random.choice(np.arange(61,76),size=5,replace=False)

    bingo_card = np.column_stack((column_1,column_2,column_3,column_4,column_5))
    bingo_card[2,2] = 9999

    return bingo_card

def scratch(bingo_card, number):
    loc = np.where(bingo_card == number)

    # If found, replace it with 9999
    if loc[0].size > 0:
        r, c = loc[0][0], loc[1][0]  # get the first (and only) occurrence
        bingo_card[r, c] = 9999

def bingo(bingo_card):
    # Check rows
    for row in bingo_card:
        if np.all(row == 9999):
            return True

    # Check columns
    for col in bingo_card.T:  # transpose to iterate over columns
        if np.all(col == 9999):
            return True

    # Check main diagonal (top-left to bottom-right)
    if np.all(np.diag(bingo_card) == 9999):
        return True

    # Check anti-diagonal (top-right to bottom-left)
    if np.all(np.diag(np.fliplr(bingo_card)) == 9999):
        return True

    # No bingo found
    return False


def simulate_single_card(n_simulations=10000):
    counter = []
    all_numbers = np.arange(1, 76)

    for _ in range(n_simulations):
        card = create_bingo_card()
        np.random.shuffle(all_numbers)
        for i, number in enumerate(all_numbers, start=1):
            scratch(card, number)
            if bingo(card):
                counter.append(i)
                break
    return np.mean(counter)


def simulate_multiple_cards(n_cards=500, n_simulations=1000):
    calls_needed = []
    all_numbers = np.arange(1, 76)

    for _ in range(n_simulations):
        cards = [create_bingo_card() for _ in range(n_cards)]
        np.random.shuffle(all_numbers)
        for i, number in enumerate(all_numbers, start=1):
            for card in cards:
                scratch(card, number)
            if any(bingo(card) for card in cards):
                calls_needed.append(i)
                break
    return np.mean(calls_needed)

def main():
    #avg_calls_single = simulate_single_card()
    #print(f"Average calls for a single card: {avg_calls_single:.2f}")
    avg_calls_any = simulate_multiple_cards()
    print(f"Average calls for 500 cards: {avg_calls_any:.2f}")

if __name__ == "__main__":
    main()

