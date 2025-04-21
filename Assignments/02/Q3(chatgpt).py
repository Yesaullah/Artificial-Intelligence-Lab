import time

class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.possible_values = [[set(range(1, 10)) if cell == 0 else {cell} for cell in row] for row in grid]

    def is_complete(self):
        return all(len(self.possible_values[i][j]) == 1 for i in range(9) for j in range(9))

    def get_possible_values(self, row, col):
        return list(self.possible_values[row][col])

    def set_possible_values(self, row, col, values):
        self.possible_values[row][col] = set(values)

    def set_element(self, row, col, value):
        self.possible_values[row][col] = {value}

    def get_element(self, row, col):
        vals = self.possible_values[row][col]
        return next(iter(vals)) if len(vals) == 1 else 0

    def get_neighbors(self, row, col):
        neighbors = set()
        for i in range(9):
            if i != col:
                neighbors.add((row, i))
            if i != row:
                neighbors.add((i, col))
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != (row, col):
                    neighbors.add((i, j))
        return list(neighbors)

    def deep_copy(self):
        new_grid = [[self.get_element(i, j) for j in range(9)] for i in range(9)]
        return Sudoku(new_grid)

    def display(self):
        for i in range(9):
            row = [str(self.get_element(i, j)) if self.get_element(i, j) != 0 else '.' for j in range(9)]
            print(' '.join(row))


class SudokuCSP:
    def __init__(self, sudoku):
        self.sudoku = sudoku

    def get_initial_sudoku(self):
        return self.sudoku.deep_copy()

    def select_unassigned_variable(self, assignment):
        # MRV: Select the variable with the fewest possible values
        min_domain_size = float('inf')
        selected_variable = None

        for i in range(9):
            for j in range(9):
                if len(assignment.get_possible_values(i, j)) > 1:  # Only consider unassigned cells
                    domain_size = len(assignment.get_possible_values(i, j))
                    if domain_size < min_domain_size:
                        min_domain_size = domain_size
                        selected_variable = (i, j)

        return selected_variable

    def order_domain_values(self, var, assignment):
        return assignment.get_possible_values(var[0], var[1])

    def is_consistent(self, var, value, assignment):
        for neighbor in assignment.get_neighbors(var[0], var[1]):
            neighbor_vals = assignment.get_possible_values(neighbor[0], neighbor[1])
            if len(neighbor_vals) == 1 and neighbor_vals[0] == value:
                return False
        return True


def backtracking_search(csp):
    assignment = csp.get_initial_sudoku()
    return recursive_backtracking(assignment, csp)

def recursive_backtracking(assignment, csp):
    if assignment.is_complete():
        return assignment

    var = csp.select_unassigned_variable(assignment)
    if var is None:
        return False

    for value in csp.order_domain_values(var, assignment):
        if csp.is_consistent(var, value, assignment):
            assignment_copy = assignment.deep_copy()
            assignment_copy.set_element(var[0], var[1], value)

            result = recursive_backtracking(assignment_copy, csp)
            if result:
                return result

    return False

def arc_consistency_3(sudoku, arcs=None):
    if arcs is None:
        arcs = []
        for row in range(9):
            for col in range(9):
                neighbors = sudoku.get_neighbors(row, col)
                for neighbor in neighbors:
                    arcs.append(((row, col), neighbor))

    while arcs:
        (xi, xj) = arcs.pop(0)
        if revise(sudoku, xi, xj):
            if len(sudoku.get_possible_values(xi[0], xi[1])) == 0:
                return False
            neighbors = sudoku.get_neighbors(xi[0], xi[1])
            neighbors.remove(xj)
            for xk in neighbors:
                arcs.append((xk, xi))
    return True

def revise(sudoku, xi, xj):
    revised = False
    xi_domain = sudoku.get_possible_values(xi[0], xi[1])
    xj_domain = sudoku.get_possible_values(xj[0], xj[1])

    for x in xi_domain[:]:
        if len(xj_domain) == 1 and xj_domain[0] == x:
            xi_domain.remove(x)
            revised = True

    if revised:
        sudoku.set_possible_values(xi[0], xi[1], xi_domain)

    return revised

# main.py
if __name__ == "__main__":
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    # Start the timer
    start_time = time.time()

    sudoku = Sudoku(puzzle)
    arc_consistency_3(sudoku)
    csp = SudokuCSP(sudoku)
    solution = backtracking_search(csp)

    # End the timer
    end_time = time.time()

    if solution:
        solution.display()
    else:
        print("No solution found.")

    # Print execution time
    print(f"Execution time: {end_time - start_time:.4f} seconds")
