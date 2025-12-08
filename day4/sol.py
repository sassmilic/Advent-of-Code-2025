
#
# Part 1
#
GRID = []
total = 0
for line in open("input.txt").readlines():
    GRID.append(line.strip())

n = len(GRID)
m = len(GRID[0])

def get_neighbors(i, j):
    rows_to_check = []
    cols_to_check = []

    for r in [i-1, i, i+1]:
        for c in [j-1, j, j+1]:
            if 0 <= r and r < n and 0 <= c and c < m:
                if not (r == i and c == j) and GRID[r][c] == '@':
                    rows_to_check.append(r)
                    cols_to_check.append(c)

    #print(list(zip(rows_to_check, cols_to_check)))
    return zip(rows_to_check, cols_to_check)

for i,row in enumerate(GRID):
    for j,x in enumerate(row):

        if x == '@' and len(list(get_neighbors(i, j))) < 4:
            total += 1

print(total)

#
# Part 2
#
GRID = []
TOTAL = 0
for line in open("input00.txt").readlines():
    GRID.append(list(line.strip()))

n = len(GRID)
m = len(GRID[0])

print("O(nm) =", n*m)

total_can_remove_calls = 0

def get_neighbors(i, j):
    rows_to_check = []
    cols_to_check = []

    for r in [i-1, i, i+1]:
        for c in [j-1, j, j+1]:
            if 0 <= r and r < n and 0 <= c and c < m:
                if not (r == i and c == j) and GRID[r][c] == '@':
                    rows_to_check.append(r)
                    cols_to_check.append(c)

    #print(list(zip(rows_to_check, cols_to_check)))
    return zip(rows_to_check, cols_to_check)

def can_remove(i, j):
    global total_can_remove_calls
    total_can_remove_calls += 1
    return GRID[i][j] == '@' and len(list(get_neighbors(i, j))) < 4

def recursive_remove(i, j):
    GRID[i][j] = '.'
    total_removed = 1
    for coor in get_neighbors(i, j):
        if can_remove(*coor):
            total_removed += recursive_remove(*coor)
    return total_removed

for i,row in enumerate(GRID):
    for j,x in enumerate(row):
        #print(i, j, x)
        if x == '@' and can_remove(i, j):
            TOTAL += recursive_remove(i, j)

print(TOTAL)
