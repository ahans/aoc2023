from math import prod
import re

p1, p2 = 0, 0
for line in open("../inputs/02.txt").read().strip().split("\n"):
    game, rounds = line.split(":")
    rgb = [
        (max(int(c) for c in re.findall(r"(\d+) " + color, rounds)), max_count)
        for color, max_count in (("r", 12), ("g", 13), ("b", 14))
    ]
    p1 += int(game.split()[1]) if all(c <= m for c, m in rgb) else 0
    p2 += prod(cm[0] for cm in rgb)

print(p1)
print(p2)
