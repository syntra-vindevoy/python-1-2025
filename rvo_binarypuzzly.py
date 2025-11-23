grid = [
    [None, None, None, 0, 1, None, None, None, None, None],
    [None, None, None, None, None, None, 0, None, None, 1],
    [None, None, 1, None, None, None, None, None, 0, None],
    [0, None, None, None, None, None, None, None, None, 1],
    [None, None, None, None, 1, None, None, None, None, None],
    [None, 1, None, None, None, None, None, 0, None, None],
    [None, None, None, None, None, None, None, None, 1, None],
    [None, None, 0, None, None, None, None, None, None, None],
    [None, None, None, None, None, 1, None, None, None, None],
    [1, None, None, None, None, None, None, None, None, 0],
]


import numpy as np

print(np.matrix(grid))


def solve():
    global grid
    for i in range(10):
        for j in range(10):
            if grid[i][j] == None:
                for n in [0, 1]:
                    if possible2(i, j, n):
                        grid[i][j] = n
                        result = solve()
                        if result is not None:
                            return result
                        grid[i][j] = None
                return None
    print(np.matrix(grid))
    return np.matrix(grid)


def possible(y, x, n):
    global grid
    if y == 0 and x == 0:
        if (grid[y + 1][x] == n and grid[y + 2][x] == n) or (
            grid[y][x + 1] == n and grid[y][x + 2] == n
        ):
            return False
    elif y == 0 and x == 1:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif y == 1 and x == 0:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
        ):
            return False
    elif y == 1 and x == 1:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif x == 9 and y == 0:
        if (grid[y + 1][x] == n and grid[y + 2][x] == n) or (
            grid[y][x - 1] == n and grid[y][x - 2] == n
        ):
            return False
    elif x == 9 and y == 1:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
        ):
            return False
    elif x == 8 and y == 0:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif x == 8 and y == 1:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif x == 0 and y == 9:
        if (grid[y - 1][x] == n and grid[y - 2][x] == n) or (
            grid[y][x + 1] == n and grid[y][x + 2] == n
        ):
            return False
    elif x == 1 and y == 9:
        if (
            (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif x == 0 and y == 8:
        if (
            (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
        ):
            return False
    elif x == 1 and y == 8:
        if (
            (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif x == 9 and y == 9:
        if (grid[y - 1][x] == n and grid[y - 2][x] == n) or (
            grid[y][x - 1] == n and grid[y][x - 2] == n
        ):
            return False
    elif x == 9 and y == 8:
        if (
            (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
        ):
            return False
    elif x == 8 and y == 9:
        if (
            (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    elif x == 8 and y == 8:
        if (
            (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
            or (grid[y - 1][x] == n and grid[y + 1][x] == n)
        ):
            return False
    elif x < 2:
        if x == 0:
            if (
                (grid[y][x + 1] == n and grid[y][x + 2] == n)
                or (grid[y - 1][x] == n and grid[y - 2][x] == n)
                or (grid[y + 1][x] == n and grid[y + 2][x] == n)
                or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            ):
                return False
        elif x == 1:
            if (
                (grid[y][x - 1] == n and grid[y][x + 1])
                or (grid[y][x + 1] == n and grid[y][x + 2] == n)
                or (grid[y - 1][x] == n and grid[y - 2][x] == n)
                or (grid[y + 1][x] == n and grid[y + 2][x] == n)
                or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            ):
                return False
    elif x > 7:
        if x == 9:
            if (
                (grid[y][x - 1] == n and grid[y][x - 2] == n)
                or (grid[y - 1][x] == n and grid[y - 2][x] == n)
                or (grid[y + 1][x] == n and grid[y + 2][x] == n)
                or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            ):
                return False
        elif x == 8:
            if (
                (grid[y][x - 1] == n and grid[y][x + 1] == n)
                or (grid[y][x - 1] == n and grid[y][x - 2] == n)
                or (grid[y - 1][x] == n and grid[y - 2][x] == n)
                or (grid[y + 1][x] == n and grid[y + 2][x] == n)
                or (grid[y - 1][x] == n and grid[y + 1][x] == n)
            ):
                return False
    elif y < 2:
        if y == 0:
            if (
                (grid[y + 1][x] == n and grid[y + 2][x] == n)
                or (grid[y][x - 1] == n and grid[y][x - 2] == n)
                or (grid[y][x - 1] == n and grid[y][x + 1] == n)
                or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            ):
                return False
        elif y == 1:
            if (
                (grid[y + 1][x] == n and grid[y - 1][x] == n)
                or (grid[y + 1][x] == n and grid[y + 2][x] == n)
                or (grid[y][x - 1] == n and grid[y][x - 2] == n)
                or (grid[y][x - 1] == n and grid[y][x + 1] == n)
                or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            ):
                return False
    elif y > 7:
        if y == 9:
            if (
                (grid[y - 1][x] == n and grid[y - 2][x] == n)
                or (grid[y][x - 1] == n and grid[y][x - 2] == n)
                or (grid[y][x + 1] == n and grid[y][x + 2] == n)
                or (grid[y][x - 1] == n and grid[y][x + 1] == n)
            ):
                return False
        if y == 8:
            if (
                (grid[y + 1][x] == n and grid[y - 1][x] == n)
                or (grid[y - 1][x] == n and grid[y - 2][x] == n)
                or (grid[y][x - 1] == n and grid[y][x - 2] == n)
                or (grid[y][x + 1] == n and grid[y][x + 2] == n)
                or (grid[y][x - 1] == n and grid[y][x + 1] == n)
            ):
                return False
    else:
        if (
            (grid[y + 1][x] == n and grid[y + 2][x] == n)
            or (grid[y + 1][x] == n and grid[y - 1][x] == n)
            or (grid[y - 1][x] == n and grid[y - 2][x] == n)
            or (grid[y][x - 1] == n and grid[y][x - 2] == n)
            or (grid[y][x + 1] == n and grid[y][x + 2] == n)
            or (grid[y][x - 1] == n and grid[y][x + 1] == n)
        ):
            return False
    return True


def possible2(y, x, n):
    global grid
    # Temporarily set the cell to n for validation
    old = grid[y][x]
    grid[y][x] = n

    # First, use your original possible() to check triples
    if not possible(y, x, n):
        grid[y][x] = old
        return False

    # Now check counts and uniqueness only if row/column is fully filled (no None)
    row = grid[y]
    col = [grid[i][x] for i in range(10)]

    # Check that counts of 0 and 1 in row and column do not exceed 5 at any point
    if row.count(0) > 5 or row.count(1) > 5 or col.count(0) > 5 or col.count(1) > 5:
        grid[y][x] = old
        return False

    # If row is fully filled, check exact counts and uniqueness
    if None not in row:
        if row.count(0) != 5 or row.count(1) != 5:
            grid[y][x] = old
            return False
        # Check uniqueness among all other rows
        for r in range(10):
            if r != y and grid[r] == row:
                grid[y][x] = old
                return False

    # If column is fully filled, check exact counts and uniqueness
    if None not in col:
        if col.count(0) != 5 or col.count(1) != 5:
            grid[y][x] = old
            return False
        # Check uniqueness among all other columns
        for c in range(10):
            if c != x:
                other_col = [grid[i][c] for i in range(10)]
                if other_col == col:
                    grid[y][x] = old
                    return False

    # Restore the original value
    grid[y][x] = old
    return True


solved_grid = solve()
