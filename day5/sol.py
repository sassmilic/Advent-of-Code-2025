#
# Part 1
#

text = open('input.txt').read()
ranges0 = [list(map(int, r.split('-'))) for r in text.split('\n\n')[0].split()]
ids = list(map(int, text.split('\n\n')[1].split()))

# sort ranges (by 1st element in tuple)
ranges0.sort()
#print(ranges0)

# merge ranges
curr = ranges0[0]
ranges = []
for i,t in enumerate(ranges0[1:]):
    if curr[1] < t[0]:
        # no overlap
        ranges.append(curr)
        curr = t
    elif curr[1] < t[1]:
        curr[1] = t[1]
ranges.append(curr)

total = 0

for x in ids:
    # binary search
    i, j = 0, len(ranges)
    while i != j:
        m = (j + i) // 2
        l, h = ranges[m][0], ranges[m][1]
        if x < l:
            j = m
        elif h < x:
            i = m + 1 
        elif l <= x and x <= h:
            total += 1
            break

print(total)

#
# Part 2
#
print(sum(y - x + 1 for (x, y) in ranges))
