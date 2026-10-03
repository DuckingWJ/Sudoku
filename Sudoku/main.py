
GRID = [
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [0, 0, 0, 1, 1, 1, 2, 2, 2],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [3, 3, 3, 4, 4, 4, 5, 5, 5],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
    [6, 6, 6, 7, 7, 7, 8, 8, 8],
    [6, 6, 6, 7, 7, 7, 8, 8, 8]
]

def checkSudoku(mp):
    row = [set() for _ in range(9)]
    col = [set() for _ in range(9)]
    grid = [set() for _ in range(9)]
    for i in range(9):
        for j in range(9):
            if 1 <= mp[i][j] <= 9:
                row[i].add(mp[i][j])
                col[j].add(mp[i][j])
                grid[GRID[i][j]].add(mp[i][j])
    for i in range(9):
        if len(row[i]) != 9 or len(col[i]) != 9 or len(grid[i]) != 9:
            return False
    return True



ans_mp = [[0 for _ in range(9)] for _ in range(9)]
mp = [[0 for _ in range(9)] for _ in range(9)]
row_mp = [[False for _ in range(10)] for _ in range(9)]
col_mp = [[False for _ in range(10)] for _ in range(9)]
grid_mp = [[False for _ in range(10)] for _ in range(9)]
blank = []
  
def dfs(remain):
    if remain == 0:
        ans_mp[:] = [row[:] for row in mp]
        return True
    
    # Find the blank cell with the maximum constraints applied
    x = y = mask = 0
    for r, c in blank:
        if mp[r][c] == 0:
            if sum(row_mp[r][1:10]) + sum(col_mp[c][1:10]) + sum(grid_mp[GRID[r][c]][1:10]) > mask:
                x, y, mask = r, c, sum(row_mp[r][1:10]) + sum(col_mp[c][1:10]) + sum(grid_mp[GRID[r][c]][1:10])
    
    # Try placing numbers 1-9 in the selected blank cell
    for i in range(1, 10):
        if not row_mp[x][i] and not col_mp[y][i] and not grid_mp[GRID[x][y]][i]:
            row_mp[x][i] = col_mp[y][i] = grid_mp[GRID[x][y]][i] = True
            mp[x][y] = i
            if dfs(remain - 1):
                return True
            row_mp[x][i] = col_mp[y][i] = grid_mp[GRID[x][y]][i] = False
            mp[x][y] = 0
    return False

def sudoku():
    blank.clear()
    ans_mp[:] = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(9):
        for j in range(1, 10):
            row_mp[i][j] = False
            col_mp[i][j] = False
            grid_mp[i][j] = False
    for i in range(9):
        for j in range(9):
            if mp[i][j] == 0:
                blank.append((i, j))
            else:
                row_mp[i][mp[i][j]] = True
                col_mp[j][mp[i][j]] = True
                grid_mp[GRID[i][j]][mp[i][j]] = True
    #
    return dfs(len(blank))