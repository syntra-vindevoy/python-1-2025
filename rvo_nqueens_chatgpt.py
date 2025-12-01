""" chatgpt solution using sets """
import numpy as np

grid = [[0]*8 for _ in range(8)]

# sets to track threatened columns and diagonals
cols = set()
diag1 = set()  # y - x
diag2 = set()  # y + x

def solve(row=0):
    if row == 8:
        return [r[:] for r in grid]  # deep copy

    for col in range(8):
        d1 = row - col
        d2 = row + col

        # check if threatened
        if col in cols or d1 in diag1 or d2 in diag2:
            continue

        # place queen
        grid[row][col] = 1
        cols.add(col)
        diag1.add(d1)
        diag2.add(d2)

        result = solve(row + 1)
        if result:
            return result

        # backtrack
        grid[row][col] = 0
        cols.remove(col)
        diag1.remove(d1)
        diag2.remove(d2)

    return None

solution = solve()
print(np.matrix(solution))

