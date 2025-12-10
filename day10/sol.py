import math
from collections import deque

filename = "input.txt"

#
# Part 1
#
def convert_to_tuple(diagram):
    diagram = diagram.strip('[]')
    return tuple(i for i, ch in enumerate(diagram) if ch == '#')

diagrams, buttons = zip(*[(convert_to_tuple(line.split()[0]), list(map(eval, line.split()[1:-1]))) for line in open(filename).readlines()])
# make sure everything in `buttons` is a tuple
buttons = tuple(
    tuple((x,) if isinstance(x, int) else x for x in group)
    for group in buttons
)

#print(diagrams)
#print(buttons)

def xor(t1, t2):
    result = []
    for x in t1:
        if x not in t2:
            result.append(x)
    for x in t2:
        if x not in t1:
            result.append(x)
    result.sort()
    return tuple(result)

def fewest_presses(start, buttons, goal):
    #print(start, buttons, goal)
    if start == goal:
        return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        board, depth = queue.popleft()
        for b in buttons:
            next_board = xor(board, b)
            #print("next board:", next_board)
            if next_board == goal:
                return depth + 1
            if next_board not in visited:
                visited.add(next_board)
                queue.append((next_board, depth + 1))
    return math.inf  # unreachable

print(sum([fewest_presses(tuple(), buttons[i], board) for i,board in enumerate(diagrams)]))

#
# Part 2
#

# linear optimization
import pyomo.environ as pyo

joltages = [eval(line.split()[-1].replace('{', '[').replace('}', ']')) for line in open(filename).readlines()]

result = 0

def expand(tup, dim):
    v = [0]*dim
    for idx in tup:
        v[idx] = 1
    return v

result = 0
for i,jolt in enumerate(joltages):
    V = jolt
    dim = len(V)

    X = [expand(t, dim) for t in buttons[i]]
    n = len(buttons[i])

    model = pyo.ConcreteModel()
    model.c = pyo.Var(range(n), domain=pyo.NonNegativeIntegers)

    # constraints
    model.eq = pyo.ConstraintList()
    for j in range(dim):
        model.eq.add(sum(model.c[i] * X[i][j] for i in range(n)) == V[j])
    
    # objective
    model.obj = pyo.Objective(expr=sum(model.c[i] for i in range(n)))

    solver = pyo.SolverFactory("cbc")
    solver.solve(model)

    result += sum(model.c[i].value for i in range(n))

print(result)
