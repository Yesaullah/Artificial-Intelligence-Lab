import time
from ortools.sat.python import cp_model

# Initial board
grid = [
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

def runsolver():
    m = cp_model.CpModel()
    vals = []

    for r in range(9):
        temp = []
        for c in range(9):
            if grid[r][c] == 0:
                temp.append(m.NewIntVar(1, 9, f'v{r}{c}'))
            else:
                temp.append(m.NewConstant(grid[r][c]))
        vals.append(temp)

    for r in vals:
        m.AddAllDifferent(r)
    for c in range(9):
        m.AddAllDifferent([vals[r][c] for r in range(9)])
    for a in range(3):
        for b in range(3):
            square = [vals[a*3+i][b*3+j] for i in range(3) for j in range(3)]
            m.AddAllDifferent(square)

    s = cp_model.CpSolver()
    t1 = time.time()
    out = s.Solve(m)
    t2 = time.time()

    if out in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        for r in vals:
            print(" ".join(str(s.Value(x)) for x in r))
        print(f"\ntime used: {t2 - t1:.4f} seconds")
    else:
        print("no result found")

runsolver()
