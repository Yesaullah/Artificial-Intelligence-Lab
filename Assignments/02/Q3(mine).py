from queue import Queue
from copy import deepcopy
import time

# Initial board
sudokuinput = [
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

def createdomains(grid):
    dom = {}
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                dom[(x, y)] = list(range(1, 10))
            else:
                dom[(x, y)] = [grid[x][y]]
    return dom

def getrelated(x, y):
    links = set()
    for i in range(9):
        if i != x:
            links.add((i, y))
        if i != y:
            links.add((x, i))
    rowstart, colstart = 3 * (x // 3), 3 * (y // 3)
    for i in range(rowstart, rowstart + 3):
        for j in range(colstart, colstart + 3):
            if (i, j) != (x, y):
                links.add((i, j))
    return links

def ac3(dom, neighborfunc):
    q = Queue()
    for i in range(9):
        for j in range(9):
            for near in neighborfunc(i, j):
                q.put(((i, j), near))
    while not q.empty():
        current, other = q.get()
        result = revise(current, other, dom)
        if result == -1:
            continue
        if result == 0:
            return False
        if result == 1:
            for link in neighborfunc(current[0], current[1]):
                q.put((link, current))
    return True

def revise(a, b, dom):
    changed = False
    if len(dom[b]) == 1:
        fixed = dom[b][0]
        if fixed in dom[a]:
            dom[a] = [v for v in dom[a] if v != fixed]
            changed = True
    if len(dom[a]) == 0:
        return 0
    return 1 if changed else -1

def backtrack(grid, dom):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                for val in dom[(x, y)]:
                    conflict = False
                    for other in getrelated(x, y):
                        if grid[other[0]][other[1]] == val:
                            conflict = True
                            break
                    if not conflict:
                        tempgrid = deepcopy(grid)
                        tempgrid[x][y] = val
                        tempdom = deepcopy(dom)
                        tempdom[(x, y)] = [val]
                        if ac3(tempdom, getrelated):
                            final = backtrack(tempgrid, tempdom)
                            if final:
                                return final
                return False
    return grid

def solve():
    puzzle = deepcopy(sudokuinput)
    doms = createdomains(puzzle)
    if ac3(doms, getrelated):
        solved = backtrack(puzzle, doms)
        if solved:
            for line in solved:
                print(" ".join(str(n) for n in line))
        else:
            print("no answer found")
    else:
        print("constraints invalid")

if __name__ == "__main__":
    begin = time.time()
    solve()
    end = time.time()
    print(f"\nsolved in {end - begin:.4f} seconds")
