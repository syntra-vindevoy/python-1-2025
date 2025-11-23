import numpy as np

grid = [
    [None, None, None, 0,    1,    None, None, None, None, None],
    [None, None, None, None, None, None, 0,    None, None, 1],
    [None, None, 1,    None, None, None, None, None, 0,    None],
    [0,    None, None, None, None, None, None, None, None, 1],
    [None, None, None, None, 1,    None, None, None, None, None],
    [None, 1,    None, None, None, None, None, 0,    None, None],
    [None, None, None, None, None, None, None, None, 1,    None],
    [None, None, 0,    None, None, None, None, None, None, None],
    [None, None, None, None, None, 1,    None, None, None, None],
    [1,    None, None, None, None, None, None, None, None, 0]
]


def print_grid():
    print(np.matrix(grid))

def check_triples(y, x, n):
    # Check row triples around (y,x)
    row = grid[y]
    for c in range(max(0, x-2), min(8, x+1)):
        triple = row[c:c+3]
        if None not in triple and triple[0] == triple[1] == triple[2] == n:
            return False
    # Check column triples around (y,x)
    col = [grid[r][x] for r in range(10)]
    for r in range(max(0, y-2), min(8, y+1)):
        triple = col[r:r+3]
        if None not in triple and triple[0] == triple[1] == triple[2] == n:
            return False
    return True

def possible2(y, x, n):
    global grid
    old = grid[y][x]
    grid[y][x] = n

    # Check no three identical in a row/column
    if not check_triples(y, x, n):
        grid[y][x] = old
        return False

    row = grid[y]
    col = [grid[i][x] for i in range(10)]

    # Counts cannot exceed 5 at any time
    if row.count(0) > 5 or row.count(1) > 5 or col.count(0) > 5 or col.count(1) > 5:
        grid[y][x] = old
        return False

    # If row is fully filled, counts must be exactly 5 and unique among rows
    if None not in row:
        if row.count(0) != 5 or row.count(1) != 5:
            grid[y][x] = old
            return False
        for r in range(10):
            if r != y and grid[r] == row:
                grid[y][x] = old
                return False

    # If column is fully filled, counts must be exactly 5 and unique among columns
    if None not in col:
        if col.count(0) != 5 or col.count(1) != 5:
            grid[y][x] = old
            return False
        for c in range(10):
            if c != x:
                other_col = [grid[i][c] for i in range(10)]
                if other_col == col:
                    grid[y][x] = old
                    return False

    grid[y][x] = old
    return True

def solve():
    global grid
    for i in range(10):
        for j in range(10):
            if grid[i][j] is None:
                for n in [0,1]:
                    if possible2(i, j, n):
                        grid[i][j] = n
                        result = solve()
                        if result is not None:
                            return result
                        grid[i][j] = None
                return None
    return grid

print("Initial grid:")
print_grid()
print("\nSolving...\n")

solved = solve()

if solved:
    print("Solution found:")
    print(np.matrix(solved))
else:
    print("No solution found.")
