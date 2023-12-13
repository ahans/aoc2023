import sys
import numpy as np

grids = [
    np.array([[int(x) for x in l] for l in p.replace(".", "0").replace("#", "1").split("\n")])
    for p in sys.stdin.read().strip().split("\n\n")
]

for diffs in (0, 1):
    s = 0
    for g in grids:
        for g, f in ((g, 1), (g.T, 100)):
            for c in range(0, g.shape[1] - 1):
                l = min(c + 1, g.shape[1] - c - 1)
                a = np.flip(g[:, c - l + 1 : c + 1], axis=1)
                b = g[:, c + 1 : c + 1 + l]
                if np.sum(a != b) == diffs:
                    s += (c + 1) * f
                    break
    print(s)
