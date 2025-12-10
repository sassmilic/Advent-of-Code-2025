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


