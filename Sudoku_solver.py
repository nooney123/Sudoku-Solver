import numpy as np
from collections import defaultdict

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.size = 9
        self.box_size = 3
        self.domains = self.initialize_domains()
        self.constraints = self.create_constraints()

    def initialize_domains(self):
        domains = {}
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    domains[(row, col)] = set(range(1, 10))
                else:
                    domains[(row, col)] = {self.board[row][col]}
        return domains

    def create_constraints(self):
        constraints = defaultdict(set)
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(row, col, num):
                            constraints[(row, col)].add(num)
        return constraints

    def is_valid(self, row, col, num):
        # Check row and column
        for x in range(self.size):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False

        # Check box
        start_row = row - row % self.box_size
        start_col = col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty(self):
        empty_cells = [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row][col] == 0]
        if not empty_cells:
            return None
        # Heuristic: Minimum Remaining Values (MRV)
        return min(empty_cells, key=lambda cell: len(self.domains[cell]))

    def backtrack(self):
        empty = self.find_empty()
        if not empty:
            return True  # Puzzle solved
        row, col = empty

        for num in self.domains[(row, col)]:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                old_domains = self.domains.copy()
                self.update_domains(row, col, num, remove=False)

                if self.backtrack():
                    return True

                # Backtrack
                self.board[row][col] = 0
                self.domains = old_domains  # Restore domains

        return False

    def update_domains(self, row, col, num, remove=True):
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) != (row, col) and (r == row or c == col or (r // self.box_size == row // self.box_size and c // self.box_size == col // self.box_size)):
                    if remove and num in self.domains[(r, c)]:
                        self.domains[(r, c)].remove(num)
                    elif not remove and num not in self.domains[(r, c)] and self.is_valid(r, c, num):
                        self.domains[(r, c)].add(num)

    def solve(self):
        if self.backtrack():
            return True
        return False

    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))

# Example Sudoku puzzle (0 represents empty cells)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0 ],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solver = SudokuSolver(sudoku_board)
if solver.solve():
    solver.print_board()
else:
    print("No solution exists")