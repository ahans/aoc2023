import sys

grid = sys.stdin.read().strip().splitlines()
H = len(grid)
W = len(grid[0])


def energize(start):
    energized = set()
    seen = set()
    positions = [start]
    while positions:
        elem = positions.pop()
        if elem in seen:
            continue
        seen.add(elem)
        y, x, dy, dx = elem
        if y < 0 or y >= H or x < 0 or x >= W:
            continue

        energized.add((y, x))

        c = grid[y][x]

        if c == ".":
            positions.append((y + dy, x + dx, dy, dx))

        else:
            if c == "\\":
                if dy == 0 and dx == 1:
                    dy, dx = 1, 0
                elif dy == 0 and dx == -1:
                    dy, dx = -1, 0
                elif dy == 1 and dx == 0:
                    dy, dx = 0, 1
                elif dy == -1 and dx == 0:
                    dy, dx = 0, -1
                positions.append((y + dy, x + dx, dy, dx))
            elif c == "/":
                if dy == 0 and dx == 1:
                    dy, dx = -1, 0
                elif dy == 0 and dx == -1:
                    dy, dx = 1, 0
                elif dy == 1 and dx == 0:
                    dy, dx = 0, -1
                elif dy == -1 and dx == 0:
                    dy, dx = 0, 1
                positions.append((y + dy, x + dx, dy, dx))
            elif c == "-":
                if dy == 0:  # passes through
                    positions.append((y + dy, x + dx, dy, dx))
                else:
                    positions.append((y, x + 1, 0, 1))
                    positions.append((y, x - 1, 0, -1))
            elif c == "|":
                if dx == 0:  # passes through
                    positions.append((y + dy, x + dx, dy, dx))
                else:
                    positions.append((y - 1, x, -1, 0))
                    positions.append((y + 1, x, 1, 0))
    return len(energized)


print(energize((0, 0, 0, 1)))
p2 = max(energize((0, x, 1, 0)) for x in range(W))
p2 = max(p2, max(energize((H - 1, x, -1, 0)) for x in range(W)))
p2 = max(p2, max(energize((y, 0, 1, 0)) for y in range(H)))
p2 = max(p2, max(energize((y, W - 1, -1, 0)) for y in range(H)))
print(p2)
