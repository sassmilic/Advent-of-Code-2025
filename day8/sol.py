import heapq

import math
from helpers import Heap, DisjointSet

NUM_CONNECTIONS = 1000
FILENAME = "input.txt"

dist = lambda p1, p2: math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

box_locs = [tuple(map(int, line.strip().split(','))) for line in open(FILENAME).readlines()]
loc_to_idx = {p:i for i,p in enumerate(box_locs)}

#
# Part 1
#

top_n = [] # max heap

for i, p1 in enumerate(box_locs):
    for j in range(i + 1, len(box_locs)):
        p2 = box_locs[j]

        d = dist(p1, p2)
        if len(top_n) < NUM_CONNECTIONS:
            heapq.heappush(top_n, (-d, p1, p2))
        elif -top_n[0][0] > d:
            heapq.heappop(top_n)
            heapq.heappush(top_n, (-d, p1, p2))

ds = DisjointSet(len(box_locs))

for (_, p1, p2) in top_n:
    ds.union(loc_to_idx[p1], loc_to_idx[p2])

top3 = [0, 0, 0] # min heap

for s in ds.get_all_sets():
    set_size = len(s)  # or ds.get_size(s[0])
    if set_size > top3[0]:
        heapq.heappop(top3)
        heapq.heappush(top3, set_size)

print(math.prod(top3))

#
# Part 2
#
all_distances = []
for i, p1 in enumerate(box_locs):
    for j in range(i + 1, len(box_locs)):
        p2 = box_locs[j]
        d = dist(p1, p2)
        all_distances.append((d, p1, p2))

all_distances.sort()
#print(all_distances)

ds2 = DisjointSet(len(box_locs))

for (d, p1, p2) in all_distances:
    #print(d, "\t", p1, p2)
    ds2.union(loc_to_idx[p1], loc_to_idx[p2])
    if max(ds2.size) == len(box_locs):
        break

print(p1, p2)
print(p1[0] * p2[0])

