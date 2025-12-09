import math
from collections import namedtuple, defaultdict

filename = "input.txt"
positions = [(int(line.split(',')[1]), int(line.split(',')[0])) for line in open(filename).readlines()]
#positions = [(int(line.split(',')[0]), int(line.split(',')[1])) for line in open(filename).readlines()]

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

print(biggest)

#
# Part 2
#

# store the positions of the loop boundary
# - vertical lines are stored in boundary["vertical_segments"]
# - horizontal lines are stored in boundary["horizontal_segments"]

from intervaltree import IntervalTree

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

vertical_trees = defaultdict(IntervalTree)
for col, segments in boundary["vertical"].items():
    for seg_r1, seg_r2 in segments:
        vertical_trees[col].addi(seg_r1, seg_r2 + 1, (seg_r1, seg_r2))  # +1 bc intervaltree uses half-open intervals

horizontal_trees = defaultdict(IntervalTree)
for row, segments in boundary["horizontal"].items():
    for seg_c1, seg_c2 in segments:
        horizontal_trees[row].addi(seg_c1, seg_c2 + 1, (seg_c1, seg_c2))

def on_vertical_boundary(p):
    r, c = p
    if c in vertical_trees:
        results = vertical_trees[c][r]
        if results:
            return results.pop().data 
    return None

def on_horizontal_boundary(p):
    r, c = p
    if r in horizontal_trees:
        results = horizontal_trees[r][c]
        if results:
            return results.pop().data
    return None

def intersection(t1, t2):
    # t1 and t2 are vertical segments
    t1, t2 = sorted([t1, t2])
    if t1[1] > t2[0]:
        return True
    return False

positions_set = set(positions)
max_c = 1 + max(p[1] for p in positions)

def is_in_loop(p):
    # ray casting algo
    if p in positions_set or on_vertical_boundary(p) or on_horizontal_boundary(p):
        return True
    
    r, c = p
    n_crossed_boundary = 0
    
    # Get all vertical segments to the right of point p
    # and check which ones our horizontal ray (at row r) crosses
    crossings = []
    
    for col, segments in boundary["vertical"].items():
        if col <= c:
            continue  # segment is to the left of or at our point
        for seg_r1, seg_r2 in segments:
            if seg_r1 <= r <= seg_r2:
                # ray at row r crosses this vertical segment at column col
                crossings.append((col, seg_r1, seg_r2))
    
    # Sort crossings by column (left to right)
    crossings.sort()
    
    prev_segment = None
    for col, seg_r1, seg_r2 in crossings:
        current_segment = (seg_r1, seg_r2)
        if prev_segment is None:
            n_crossed_boundary += 1
        else:
            # Check if current segment overlaps with previous
            # (meaning they're part of a connected boundary we're tracing along)
            if intersection(current_segment, prev_segment):
                n_crossed_boundary += 1
        prev_segment = current_segment
    
    return n_crossed_boundary % 2 == 1

"""
max_r = max(p[0] for p in positions)
for r in range(max_r + 1):
    for c in range(max_c):
        #print(r, c)
        if is_in_loop((r, c)):
            print("\033[32m0\033[0m", end="\t")
        else:
            print('.', end='\t')
    print()
print()
#"""

#print(is_in_loop((3, 3)))
#print(is_in_loop((2, 8)))

memo = {}
def is_all_green(p1, p2):
    if (p1, p2) in memo:
        return memo[(p1, p2)]
    if p1 == p2:
        result = is_in_loop(p1)
    elif p2[1] == p1[1]:
        # points are on the same column
        col = p1[1]
        p1, p2 = sorted([p1, p2])  # p1 is higher than p2
        # so: split in half in horizontal direction
        new_row = (p1[0] + p2[0]) // 2
        result = is_all_green(p1, (new_row, col)) and is_all_green(p2, (1 + new_row, col))
    elif p2[0] == p1[0]:
        # points are on the same row
        row = p1[0]
        p1, p2 = sorted([p1, p2])  # p1 is to the left of p2
        # so: split in half in vertical direction
        new_col = (p1[1] + p2[1]) // 2
        result = is_all_green(p1, (row, new_col)) and is_all_green(p2, (row, 1 + new_col))
    else:
        # split rectangle into 4 quadrants
        mid_row = (p1[0] + p2[0]) // 2
        mid_col = (p1[1] + p2[1]) // 2
        
        p1, p2 = sorted([p1, p2]) 
        
        # Top-left, top-right, bottom-left, bottom-right
        result = (is_all_green(p1, (mid_row, mid_col)) and
                  is_all_green((p1[0], mid_col + 1), (mid_row, p2[1])) and
                  is_all_green((mid_row + 1, p1[1]), (p2[0], mid_col)) and
                  is_all_green((mid_row + 1, mid_col + 1), p2))
    memo[(p1, p2)] = result
    return result

def area(p1, p2):
    return (1 + abs(p1[0] - p2[0])) * (1 + abs(p1[1] - p2[1]))

import itertools

import tqdm

max_area = 0
for p1,p2 in tqdm.tqdm(list(itertools.combinations(positions, 2))):
    if is_all_green(p1, p2) and area(p1, p2) > max_area:
        max_area = area(p1, p2)

print(max_area)
#print(memo)

    
