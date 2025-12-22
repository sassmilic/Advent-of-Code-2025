import re

filename = "input00.txt"

shapes = {}

# read input
f = open(filename)
line = f.readline()
while line:
    line = line.strip()
    if re.match(r"\d:", line):
        shape_num = int(line[:-1])
        shapes[shape_num] = set()
        # shape is 3 lines
        shape_indices = []
        for i,_ in enumerate(range(3)):
            line = f.readline()
            shape_indices.extend((i,j) for j,x in enumerate(line) if x == '#')
        shape_indices.sort()
        shapes[shape_num].add(tuple(shape_indices))
        # rotate 90 degrees cw three times
        for _ in range(3):
            shape_indices = [(j,3-i-1) for (i,j) in shape_indices]
            shape_indices.sort()
            shapes[shape_num].add(tuple(shape_indices))
        for shp in list(shapes[shape_num]):
            # flip all of them
            shape_indices = [(i,2-j) for (i,j) in shp]
            shape_indices.sort()
            shapes[shape_num].add(tuple(shape_indices))

    line = f.readline()

print(shapes)


