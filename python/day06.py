import sys
import math
import numpy as np


def s(times, dist):
    num_winning = []
    for d, r in zip(times, dist):
        t = np.arange(d)
        num_winning.append(np.count_nonzero(t * (d - t) > r))
    return math.prod(num_winning)


lines = open("../inputs/06.txt").read().strip().splitlines()
times = lines[0].split()[1:]
distances = lines[1].split()[1:]

print(s([int(x) for x in times], [int(x) for x in distances]))
print(s([int("".join(times))], [int("".join(distances))]))
