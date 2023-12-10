import sys

sys.setrecursionlimit(20000)

grid = [list(line.strip()) for line in sys.stdin.read().strip().splitlines()]
H = len(grid)
W = len(grid[0])

S = None
for y in range(H):
    for x in range(W):
        if grid[y][x] == "S":
            assert S is None
            S = (y, x)


def search(cur, prev, path):
    if cur == S:
        return path
    y, x = cur
    if y < 0 or x < 0 or y >= H or x >= W:
        return None
    if len(path) > 15000:
        return None

    dy, dx = y - prev[0], x - prev[1]
    match (grid[y][x], dy, dx):
        case "-", 0, dx:  # left or right
            return search((y, x + dx), cur, path + [cur])
        case "|", dy, 0:  # top or bottom
            return search((y + dy, x), cur, path + [cur])
        case "L", 0, -1:  # coming from right
            return search((y - 1, x), cur, path + [cur])
        case "L", 1, 0:  # coming from top (1, 0)
            return search((y, x + 1), cur, path + [cur])
        case "J", 0, 1:  # coming from left
            return search((y - 1, x), cur, path + [cur])
        case "J", 1, 0:  # coming from top
            return search((y, x - 1), cur, path + [cur])
        case "7", -1, 0:  # coming from bottom
            return search((y, x - 1), cur, path + [cur])
        case "7", 0, 1:  # coming from left
            return search((y + 1, x), cur, path + [cur])
        case "F", 0, -1:  # coming from right
            return search((y + 1, x), cur, path + [cur])
        case "F", -1, 0:  # coming from bottom
            return search((y, x + 1), cur, path + [cur])
    return None


for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
    path = search((S[0] + dy, S[1] + dx), S, [S])
    if path:
        print(len(path) // 2)
        break

path_set = set(path)


def floodfill(y, x):
    q = [(y, x)]
    seen = set()
    while q:
        p = q.pop()
        y, x = p
        if not p in path_set and p not in seen:
            seen.add(p)
            if 0 <= p[1] < W and 0 <= p[0] < H:
                grid[p[0]][p[1]] = "+"
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= nx < W and 0 <= ny < H:
                    q.append((ny, nx))


def right(y, x):
    return -x, y


def left(y, x):
    return x, -y


# path = list(reversed(path))
neighy, neighx = 1, 0
floodfill(S[0] + neighy, S[1] + neighx)
for p in path[1:]:
    c = grid[p[0]][p[1]]
    # print(f"pos = {p} {c} d ir={(neighy, neighx)}")
    # seed = p[0] + neighy, p[1] + neighx
    # if seed not in path_set and 0 <= seed[0] < H and 0 <= seed[1] < W:
    #     grid[seed[0]][seed[1]] = '*'
    floodfill(p[0] + neighy, p[1] + neighx)

    update = True
    match c, neighy, neighx:
        case "7", 0, _:
            neighy, neighx = right(neighy, neighx)
        case "7", _, 0:
            neighy, neighx = left(neighy, neighx)
        case "F", 0, _:
            neighy, neighx = left(neighy, neighx)
        case "F", _, 0:
            neighy, neighx = right(neighy, neighx)
        case "L", _, 0:
            neighy, neighx = left(neighy, neighx)
        case "L", 0, _:
            neighy, neighx = right(neighy, neighx)
        case "J", 0, _:
            neighy, neighx = left(neighy, neighx)
        case "J", _, 0:
            neighy, neighx = right(neighy, neighx)
        case _:
            update = False
    if update:
        floodfill(p[0] + neighy, p[1] + neighx)
        # seed = p[0] + neighy, p[1] + neighx
        # if seed not in path_set  and 0 <= seed[0] < H and 0 <= seed[1] < W:
        #     grid[seed[0]][seed[1]] = '*'


for y in range(H):
    for x in range(W):
        if grid[y][x] == "+" or (y, x) in path_set:
            continue
        grid[y][x] = "."
        # if grid[y][x] != "*" and (y, x) not in path_set:
        #     grid[y][x] = " "
# print('\n'.join([''.join(r) for r in grid]))
grid[S[0]][S[1]] = "F"
for line in grid:
    #
    print(
        "".join(line)
        .replace("F", "┌")
        .replace("7", "┐")
        .replace("J", "┘")
        .replace("L", "└")
        .replace("-", "─")
        .replace("|", "│")
    )
    # print()

n = 0
for line in grid:
    for c in line:
        if c == "+":
            n += 1
print(n)
