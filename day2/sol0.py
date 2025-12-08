result = 0


lines = open("input.txt").read().strip().split(',')
for line in lines:
    for x in range(int(line.split('-')[0]), int(line.split('-')[1]) + 1):
        x = str(x)
        if not len(x) % 2:
            i = len(x) // 2
            if x[:i] == x[i:]:
                result += int(x)

print(result)

