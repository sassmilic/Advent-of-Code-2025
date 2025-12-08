cl = 50
num_zeros = 0
for line in open('input.txt').readlines():
    line = line.strip()
    dir_ = line[0]
    x = int(line[1:])
    if dir_ == 'R':
        if cl + x >= 100:
            num_zeros += (cl + x) // 100
        cl = (cl + x) % 100
    else:
        # left
        if cl - x <= 0:
            num_zeros += 1 + abs(cl - x) // 100
            if cl == 0:
                num_zeros -= 1
        cl = (cl - x) % 100
        
print(num_zeros)


