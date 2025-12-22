import random
import re
import tqdm

filename = "input.txt"

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

# helpers for debugging
def print_shape(shape):
    for i in range(3):
        for j in range(3):
            if (i,j) in shape:
                print(f'#', end="") 
        print('\n', end="")
    print()

def print_state(state):
    for i in range(state.n):
        for j in range(state.m):
            if (i,j) in state.filled_idxs:
                print(f'#', end="")
            else:
                print(f'.', end="") 
        print('\n', end="")
    print()

# define state for backtracking algo
class State():
    def __init__(self, n, m, num_shapes):
        self.n = n
        self.m = m
        self.num_shapes = num_shapes
        self.filled_idxs = set()
    def __str__(self):
        return f"{self.n}x{self.m}: {str(self.num_shapes)}"
    def space_left(self):
        return self.n * self.m - len(self.filled_idxs)
    def is_valid(self, shape):
        # can `shape` fit into the current state
        for i in range(self.n - 2):
            for j in range(self.m - 2):
                #if (i,j) in self.filled_idxs:
                #    continue
                shape_pos = [(i+i0, j+j0) for (i0,j0) in shape] # generator
                # check all indices in shape
                if all((ii,jj) not in self.filled_idxs for (ii,jj) in shape_pos):
                    return shape_pos
        return False
    def apply(self, shape):
        for (i,j) in shape:
            self.filled_idxs.add((i,j))
    def undo(self, shape):
        for (i,j) in shape:
            self.filled_idxs.remove((i,j))

def backtrack(state):
    #print("BACKTRACK")
    #print_state(state)
    if all(x == 0 for x in state.num_shapes):
        return True

    # TODO: if no more space left => return False

    for i in range(len(state.num_shapes)):
        if state.num_shapes[i] == 0:
            continue
        for shp in shapes[i]:
            #print_shape(shp)
            #print("Checking validity...")
            shape_pos = state.is_valid(shp)
            if shape_pos:
                state.apply(shape_pos)
                state.num_shapes[i] -= 1
                if backtrack(state):
                    return True
                # undo
                state.undo(shape_pos)
                state.num_shapes[i] += 1

    return False

regions = open(filename).read().split('\n\n')[-1].split('\n')

for r in regions:
    if not r:
        continue
    #print("REGION")
    #print(r)
    l = r.split()
    dims = l[0].split('x')
    n, m = dims[0], dims[-1][:-1]
    #print(n, m)
    state = State(int(n), int(m), [int(x) for x in l[-len(shapes):]])
    #print(state)
    print(backtrack(state))

