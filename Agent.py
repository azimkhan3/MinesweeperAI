"""
For each cell:
    - maintain database of whether or not it is a mine or safe(or currently covered)
    - the number of safe squares identified around it (SAFE NEIGHBORS)
    - the number of mines identified around it (MINE NEIGHBORS)
    - the number of hidden squares around it (UNKNOWN NEIGHBORS)
"""
import numpy as np


class Minesweeper():
    """
    Minesweeper game representation
    """
#checking branches

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def neighboring_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class BaseAgent():

    def __init__(self, env=None):
        self.env = env

    def play(self):
        self.env.click_square(0, 0)
        self.env.render_env()

        old_ground = None
        current_ground = self.env.mine_ground_copy
        while not np.array_equal(old_ground, current_ground):
            old_ground = current_ground.copy()
            self._basic_solver(current_ground)
            current_ground = self.env.mine_ground_copy

    def _basic_solver(self, ground):
        for row in range(ground.shape[0]):
            for column in range(ground.shape[1]):
                if np.isnan(ground[row, column]) or self.env.flags[row, column]:
                    continue
                else:
                    if ground[row, column] == 0:
                        self._query_all_neighbours(row, column)

                    elif ground[row, column] == 8:
                        self._flag_all_neighbours(row, column)

                    else:
                        if self._get_bomb(row, column) == ground[row, column]:
                            self._query_all_neighbours(row, column)
                        elif self._get_unexplored(row, column) == ground[row, column]:
                            self._flag_all_neighbours(row, column)

    def _query_all_neighbours(self, row, column):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.env.mine_ground_copy.shape[0]
                        and column + j < self.env.mine_ground_copy.shape[1] and (
                        not self.env.flags[row + i, column + j])
                        and np.isnan(self.env.mine_ground_copy[row + i, column + j])):
                    self.env.click_square(row + i, column + j)
                    self.env.render_env()

    def _flag_all_neighbours(self, row, column):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.env.mine_ground_copy.shape[0]
                        and column + j < self.env.mine_ground_copy.shape[1] and (
                        not self.env.flags[row + i, column + j])
                        and np.isnan(self.env.mine_ground_copy[row + i, column + j])):
                    self.env.add_mine_flag(row + i, column + j)
                    self.env.render_env()

    def _get_bomb(self, row, column):
        bomb_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.env.mine_ground_copy.shape[0]
                        and column + j < self.env.mine_ground_copy.shape[1] and self.env.flags[row + i, column + j]):
                    bomb_count = bomb_count + 1
        return bomb_count

    def _get_unexplored(self, row, column):
        unexplored_count = 0
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (i == 0 and j == 0):
                    continue
                if (row + i >= 0 and column + j >= 0 and row + i < self.env.mine_ground_copy.shape[0]
                        and column + j < self.env.mine_ground_copy.shape[1] and np.isnan(
                            self.env.mine_ground_copy[row + i, column + j])):
                    unexplored_count = unexplored_count + 1
        return unexplored_count