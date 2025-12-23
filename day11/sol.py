# read input
filename = "input.txt"
graph = {}
for line in open(filename).readlines():
    line = line.strip()
    nodes = line.split()
    graph[nodes[0][:-1]] = nodes[1:]

#
# Part 1
#
memo = {}
def num_paths(node, path, blocked_set):
    if node == "out":
        return 1
    if node in memo:
        return memo[node]
    npaths = 0
    for n in graph[node]:
        if n not in path and n not in blocked_set:
            npaths += num_paths(n, path + [n], blocked_set)
    memo[node] = npaths
    return npaths

result = num_paths("svr", ["svr"], blocked_set=set())
print(result)

#
# Part 2
#

memo = {}
total = num_paths("svr", ["svr"], set())
memo = {}
dac_blocked = num_paths("svr", ["svr"], set(["dac"]))
memo = {}
fft_blocked = num_paths("svr", ["svr"], set(["fft"]))
memo = {}
both_blocked = num_paths("svr", ["svr"], set(["dac", "fft"]))

# inclusion - exclusion
result = total - dac_blocked - fft_blocked + both_blocked

print(result)
