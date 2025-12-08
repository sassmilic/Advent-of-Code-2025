
def check(x, n):
    for i in range(n):
        for j in range(len(x) // n):
            if x[i] != x[j * n + i]:
                return False
    return True


result = 0
lines = open("input.txt").read().split(',')
for line in lines:
    line = line.strip()
    for x in range(int(line.split('-')[0]), int(line.split('-')[1]) + 1):
        x = str(x)
        # max repeating segment length is half of the length of the string
        for n in range(1, 1 + len(x) // 2):
            if not len(x) % n:
                if check(x, n):
                    result += int(x)
                    #print(x)
                    break
print(result)
