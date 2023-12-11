import re

col_counts = None
row_counts = []
galaxies = []
for y, line in enumerate(open("../inputs/11.txt").read().strip().splitlines()):
    if not col_counts:
        col_counts = [0 for _ in range(len(line))]
        row_counts = col_counts[::]
    for x in [m.start() for m in re.finditer("#", line)]:
        galaxies.append((y, x))
        row_counts[y] = 1
        col_counts[x] = 1

col_counts[0] = abs(col_counts[0] - 1)
row_counts[0] = abs(row_counts[0] - 1)
for i in range(1, len(col_counts)):
    col_counts[i] = abs(col_counts[i] - 1) + col_counts[i - 1]
    row_counts[i] = abs(row_counts[i] - 1) + row_counts[i - 1]

for f in (1, 1000000 - 1):
    s = 0
    for a in range(len(galaxies) - 1):
        for b in range(a + 1, len(galaxies)):
            ay, ax = galaxies[a]
            by, bx = galaxies[b]
            ax, bx = min(ax, bx), max(ax, bx)
            s += (by - ay) + +(bx - ax) + f * (row_counts[by] - row_counts[ay] + col_counts[bx] - col_counts[ax])
    print(s)
