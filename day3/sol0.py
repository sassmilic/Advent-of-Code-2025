def max_idx(l, i=0, j=None):
    idx = i
    if not j:
        j = len(l)
    for j in range(idx, j):
        if l[j] > l[idx]:
            idx = j
    return idx

total = 0
for line in open("input.txt").readlines():
    line = line.strip()
    # find index of largest integer
    i = max_idx(line)
    if i < len(line) - 1:
        # get index of highest int to the right of i
        j = max_idx(line, i+1)
        x = int(line[i] + line[j])
    else:
        # the largest digit is last
        # get second largest number
        j = max_idx(line, j=len(line)-1)
        x = int(line[j] + line[-1])
    total += x

print(total)

