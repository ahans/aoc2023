import sys


lines = sys.stdin.read().strip().splitlines()


def solve(p2):
    y, x = 0, 0
    edges = [(0, 0)]

    for line in lines:
        d, n, rgb = line.split()
        n = int(n)
        if p2:
            dist = rgb[2:7]
            n = int(dist, 16)
            d = rgb[7]
        match (d):
            case "0" | "R":
                dy, dx = 0, 1
            case "2" | "L":
                dy, dx = 0, -1
            case "1" | "D":
                dy, dx = 1, 0
            case "3" | "U":
                dy, dx = -1, 0
        y, x = y + dy * n, x + dx * n

        edges.append((y, x))

    a = 0
    outer = 0
    for i in range(len(edges) - 1):
        a += edges[i][1] * (edges[i + 1][0] - edges[i - 1][0])
        outer += abs(edges[i + 1][0] - edges[i][0]) + abs(edges[i + 1][1] - edges[i][1])

    return a // 2 + outer // 2 + 1


print(solve(p2=False))
print(solve(p2=True))
