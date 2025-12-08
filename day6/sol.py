import math

filename = "input.txt"

# read file to get operations
ops = open(filename).readlines()[-1].split()
# keep track of totals so far
so_far = [0 if op == '+' else 1 for op in ops]

for line in open(filename).readlines()[:-1]:
    line = line.strip()

    for i,x in enumerate(line.split()):
        if ops[i] == '+':
            so_far[i] += int(x)
        else:
            # ops[i] == '*'
            so_far[i] *= int(x)

print(sum(so_far))

#
# Part 2
#

# get last line (containing operations)
with open(filename) as f:
    last = None
    for line in f:
        last = line

ops = last.split()

# precompute a bunch of necessary values from `last`

max_exp_len = []    #   max_exp_len[n]  := the maximum number of digits in any expression in equation n 
index_to_eq = []    #   index_to_eq[i]  := the equation number that the digit at index i maps to
eq_start_idx = [0]   #   eq_start_idx[n] := the starting index of equation n    

curr_max_exp_len = -1 # TODO: explain
curr_eq_number = 0
for i,ch in enumerate(last):
    if i > 0 and ch in ['+', '*']:
        eq_start_idx.append(i)
        max_exp_len.append(curr_max_exp_len)
        curr_max_exp_len = 0
        curr_eq_number += 1
    else:
        curr_max_exp_len += 1
    index_to_eq.append(curr_eq_number)
max_exp_len.append(curr_max_exp_len + 1)

#print("Max expression length:", max_exp_len)
#print("Index to equation:", index_to_eq)
#print("Equation start index:", eq_start_idx)

so_far = [[0] * l for l in max_exp_len]

with open(filename) as f:
    for line in f:
        if line == last:
            continue
        for i,digit in enumerate(line):
            if not digit.strip():
                continue
            digit = int(digit)
            # which equation is it in?
            equation_number = index_to_eq[i]
            pos = i - eq_start_idx[equation_number]
            if not so_far[equation_number][pos]:
                so_far[equation_number][pos] = digit
            else:
                so_far[equation_number][pos] = 10 * so_far[equation_number][pos] + digit

total = sum([math.prod(eq) if ops[i] == "*" else sum(eq) for (i,eq) in enumerate(so_far)])

print(total)
