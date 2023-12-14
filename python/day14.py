import sys
import numpy as np

grid = np.array(
    [
        list([int(x) for x in line.strip().replace(".", "0").replace("#", "1").replace("O", "2")])
        for line in sys.stdin.read().strip().splitlines()
    ]
)

H = grid.shape[0]
W = grid.shape[1]

load = lambda grid: sum((H - y) * np.sum(grid[y, :] == 2) for y in range(H))
seen = {}

cycle = 0
while True:
    h = grid.tobytes()

    if h in seen:
        cycle_len = cycle - seen[h]
        left = 1000000000 - cycle + 1
        skip = left // cycle_len
        cycle += skip * cycle_len
    else:
        seen[h] = cycle

    for r in range(4):
        for start_y in range(1, H):
            for x in range(W):
                if grid[start_y, x] == 2:
                    y = start_y
                    while y > 0 and grid[y - 1, x] == 0:
                        y -= 1
                    grid[y, x], grid[start_y, x] = grid[start_y, x], grid[y, x]

        if r == 0 and cycle == 0:
            print(load(grid))

        grid = np.rot90(grid, k=-1)

    cycle += 1

    if cycle == 1000000000:
        print(load(grid))
        break
