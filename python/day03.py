import re
from math import prod
from itertools import product

grid = open("../inputs/03.txt").read().split("\n")

numbers = []
pos_to_number = {}
for y, line in enumerate(grid):
    for m in re.finditer(r"\d+", line):
        numbers.append(int(m[0]))
        pos_to_number.update(
            {(x, y): len(numbers) - 1 for x in range(m.start(), m.end())}
        )

p1 = 0
p2 = 0
for y, line in enumerate(grid):
    for x, c in enumerate(line):
        if c != "." and not c.isdigit():
            neighbors = {
                pos_to_number[(nx, ny)]
                for (nx, ny) in product((x - 1, x, x + 1), (y - 1, y, y + 1))
                if (nx, ny) in pos_to_number
            }
            p1 += sum(numbers[idx] for idx in neighbors)
            if c == "*" and len(neighbors) == 2:
                p2 += prod(numbers[idx] for idx in neighbors)

print(p1)
print(p2)
