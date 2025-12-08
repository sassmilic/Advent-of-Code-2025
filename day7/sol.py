grid = []
for line in open('input.txt').readlines():
    line = line.strip()
    grid.append(line)

#
# Part 1
#
tachyon_loc = set()
tachyon_loc.add((grid[0].find('S')))

num_splits = 0

for row in grid[1:-1]:
    tachyon_loc_prime = set()
    for c in tachyon_loc:
        if row[c] == '^':
            num_splits += 1
            if c > 0:
                tachyon_loc_prime.add(c - 1)
            if c < len(row) - 1:
                tachyon_loc_prime.add(c + 1)
        else:
            tachyon_loc_prime.add(c)
 
    tachyon_loc = tachyon_loc_prime

print(num_splits)

#
# Part 2
#
start_idx = grid[0].find('S')

memo = {}

def num_timelines(r, c):

    if memo.get((r, c)):
        return memo[(r, c)]

    result = None

    if r >= len(grid) - 1:
        result = 1
    elif grid[r + 1][c] == '^':
        result = num_timelines(r + 1, c - 1) + num_timelines(r + 1, c + 1)
    else:
        result = num_timelines(r + 1, c)

    memo[(r, c)] = result
    return result

print(num_timelines(0, start_idx))
