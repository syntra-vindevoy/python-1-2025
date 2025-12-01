import numpy as np

grid = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

def possible(y,x):
    for j in range(8):
        if grid[y][j]==1: #check row
            return False
        if grid[j][x]==1: #check column
            return False
    i, j = y, x #check diagonal to the upper left
    while i>=0 and j>=0:
        if grid[i][j]==1:
            return False
        i, j = i-1, j-1
    i, j = y, x #check diagonal to the upper right
    while i>=0 and j<8:
        if grid[i][j]==1:
            return False
        i, j = i-1, j+1
    i, j = y, x #check diagonal to the lower left
    while i<8 and j>=0:
        if grid[i][j]==1:
            return False
        i, j = i+1, j-1
    i, j = y, x #check diagonal to the lower right
    while i<8 and j<8:
        if grid[i][j]==1:
            return False
        i, j = i+1, j+1
    return True

def solve(row=0):
    if row == 8:
        # return a deep copy of the solved grid, you only need to loop over the rows because you can only put one queen in a row
        return [r[:] for r in grid]

    for col in range(8):
        if possible(row, col):
            grid[row][col] = 1

            result = solve(row + 1)
            if result: #if solve return true then return result
                return result

            grid[row][col] = 0  # backtrack, als het niet

    return None  # no solution from this row

solution = solve()
print(np.matrix(solution))
