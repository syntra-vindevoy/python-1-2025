import numpy as np

puzzle = [
    [0, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, 0, np.nan, 1, np.nan],
    [1, 0, 0, 1, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0],
    [np.nan, 1, 1, np.nan, 0, 1],
    [np.nan, 1, np.nan, np.nan, 1, np.nan]
]


def check():
    assert len(puzzle) == 6
    for row in puzzle:
        assert len(row) == 6

# Print the formatted matrix
def print_puzzle():
    for row in puzzle:
        line = ""
        for val in row:
            if np.isnan(val):
                line += f"{'nan':>4}"
            else:
                line += f"{int(val):>4}"
        print(line)

def possible(row, col, value):
    for row in puzzle:
        number_0 = np.count_nonzero(row)
        number_1 = np.count_nonzero(row)

def solve():
    elements = len(puzzle)

    for row in range(elements):
        for col in range(elements):
            if puzzle[row][col] == np.nan:
                for value in range(2):
                    if possible(row, col, value):
                        puzzle[row][col] = value
                        solve()
                        puzzle[row][col] = np.nan

                    return

    return puzzle

def main():
    global puzzle

    check()

    # Convert to numpy array
    puzzle = np.array(puzzle)

    print_puzzle()


if __name__ == '__main__':
    main()