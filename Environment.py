"""
- Generate d x d grid -> store d to be referenced by agent
- Take input of n mines and randomly place them throughout grid

- For each cell:
    - check neighbors, count # of mines -> store #

"""


def environment(mines, num_rows, num_cols):  # given a # of mines, randomly assign it in grid
    cells = [[0 for i in range(num_cols)] for j in range(num_rows)]

    for mine_loc in mines:
        (mine_row, mine_col) = mine_loc
        cells[mine_row][mine_col] = -1  # if it is a bomb "place -1"

        row_range = range(mine_row - 1, mine_row + 2)
        col_range = range(mine_col - 1, mine_col + 2)

        for i in row_range:
            for j in col_range:
                if 0 <= i < num_rows and 0 <= j < num_cols and cells[i][j] != -1:
                    cells[i][j] += 1  # if in range and not a mine, then update neighbors

    return cells


print(environment([[0, 0], [1, 1]], 4, 4))
