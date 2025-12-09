import math
from collections import namedtuple, defaultdict

filename = "input0.txt"
positions = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in open(filename).readlines()]

#
# Part 1
#

Closest = namedtuple("Closest", ["top_left", "top_right", "bot_left", "bot_right"])

distance = lambda p1,p2: math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) 

min_x = min(x for (x,_) in positions)
min_y = min(y for (_,y) in positions)
max_x = max(x for (x,_) in positions)
max_y = max(y for (_,y) in positions)

top_left = (min_x, min_y)
top_right = (min_x, max_y)
bot_left = (max_x, min_y)
bot_right = (max_x, max_y)

closest = [None, None, None, None]

for p1 in positions:
    for i,p2 in enumerate([top_left, top_right, bot_left, bot_right]):
        d = distance(p1, p2)
        if not closest[i] or closest[i][0] > d:
            closest[i] = (d, p1)

#print(closest)


top_left = closest[0][1]
bot_right = closest[3][1]
width = 1 + bot_right[0] - top_left[0]
height = 1 + bot_right[1] - top_left[1]

biggest = width * height

top_right = closest[1][1]
bot_left = closest[2][1]
width = 1 + top_right[0] - bot_left[0]
height = 1 + top_right[1] - bot_left[1]

if width * height > biggest:
    biggest = width * height

#
# Part 2
#

# store the positions of the loop boundary
# - vertical lines are stored in boundary["vertical_segments"]
# - horizontal lines are stored in boundary["horizontal_segments"]
boundary = {
    "vertical"   : defaultdict(list),  # col: [(r1, r2), ...]
    "horizontal" : defaultdict(list)   # row: [(c1, c2), ...]
}
n = len(positions)
for i in range(n):
    p1, p2 = positions[i], positions[(i+1)%n]
    if p1[0] == p2[0]:
        r = p1[0]
        boundary["horizontal"][r].append(tuple(sorted([p1[1], p2[1]])))
    else:
        assert p1[1] == p2[1]
        c = p1[1]
        boundary["vertical"][c].append(tuple(sorted([p1[0], p2[0]])))

def on_boundary(p):
    # TODO: this can be made more efficient using interval trees
    # TODO: compute runtime
    r, c = p
    if r in boundary["horizontal"]:
        for segment in boundary["horizontal"][r]:
            if segment[0] <= c and c <= segment[1]:
                return True
    if c in boundary["vertical"]:
        for segment in boundary["vertical"][c]:
            if segment[0] <= r and r <= segment[1]:
                return True
    return False

positions_set = set(positions)
max_c = 1 + max(p[1] for p in positions)
def is_in_loop(p):
    # ray casting algo
    # if already on boundary, then true
    if p in positions_set or on_boundary(p):
        return True
    # cast ray to right
    r, c = p
    n_crossed_boundary = 0
    while c < max_c + 1:
        print(r, c)
        if on_boundary((r, c)):
            print("currently on boundary")
            if not on_boundary((r, c+1)):
                n_crossed_boundary += 1
        c += 1
    print(n_crossed_boundary)
    return n_crossed_boundary % 2 == 1

"""
max_r = max(p[0] for p in positions)
for r in range(max_r):
    for c in range(max_c):
        print(r, c)
        print(is_in_loop((r, c)))
"""
print(is_in_loop((2, 10)))
#def is_all_green(p1, p2):

