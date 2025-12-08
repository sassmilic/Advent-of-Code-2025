class Heap:
    def __init__(self, n):
        self._heap = [None] * n
        self._size = 0
        self._max = n

    def size(self):
        return self._size

    def find_min(self):
        if self._size == 0:
            return None
        return self._heap[0][0]

    def insert(self, x):
        if self._size < self._max:
            self._heap[self._size] = x
            self._heapify(self._size)
            self._size += 1
        else:
            raise Exception

    def _heapify(self, i):
        while i > 0 and self._heap[(i-1)//2] > self._heap[i]:
            self._heap[(i-1)//2], self._heap[i] = self._heap[i], self._heap[(i-1)//2]
            i = (i - 1) // 2

    def replace(self, x):
        # replace root with new value x
        self._heap[0] = x

        i = 0
        while i < self._size:

            if self._heap[i] <= self._heap[j]:
                break

            left, right = 2*i + 1, 2*i + 2
            if left >= self._size:
                break
            j = left if (right >= self._size or self._heap[left] < self._heap[right]) else right

            self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
            i = j

class DisjointSet:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return
        # union by size
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
    
    def get_size(self, x):
        return self.size[self.find(x)]
    
    def get_all_sets(self):
        sets = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in sets:
                sets[root] = []
            sets[root].append(i)
        return list(sets.values())

"""
# Test basic operations
h = Heap(10)

# Test 1: Empty heap
assert h.find_min() is None

# Test 2: Insert and find_min
h.insert(5)
assert h.find_min() == 5

h.insert(3)
assert h.find_min() == 3

h.insert(7)
h.insert(1)
assert h.find_min() == 1

# Test 3: Heap property maintained
h.insert(2)
h.insert(8)
h.insert(0)
assert h.find_min() == 0

# Test 4: Replace root
h.replace(4)
assert h.find_min() == 1  # Next smallest after removing 0

# Test 5: Replace with larger value
h.replace(10)
assert h.find_min() == 2

# Test 6: Fill to capacity
h2 = Heap(3)
h2.insert(5)
h2.insert(3)
h2.insert(7)

# Test 7: Overflow
try:
    h2.insert(1)
    assert False, "Should have raised Exception"
except:
    pass
"""
