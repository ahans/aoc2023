from itertools import cycle
import sys
import math


def read_input():
    instructions, n = sys.stdin.read().strip().split("\n\n")
    n = n.splitlines()
    network = {}
    for line in n:
        src, _, left, right = line.strip().replace("(", "").replace(")", "").replace(",", "").split()
        network[src] = (left, right)
    return instructions, network


def part1(instructions, network):
    node = "AAA"
    ins = cycle(instructions)
    count = 0
    while node != "ZZZ":
        left, right = network[node]
        node = left if next(ins) == "L" else right
        count += 1
    return count


def part2(instructions, network):
    s = []
    dsts = []
    for src in network.keys():
        if src[-1] == "A":
            s.append(src)
        if src[-1] == "Z":
            dsts.append(src)
    dsts = set(dsts)

    cycles = {}
    traces = {}
    for src in s:
        ins = enumerate(cycle(instructions))
        n = 0
        current = src
        seen = set()
        z_from_start = None
        traces[src] = []
        while True:
            next_i, next_ins = next(ins)
            next_i = next_i % len(instructions)
            if (current, next_i) in seen:
                break
            seen.add((current, next_i))

            next_node = network[current][0] if next_ins == "L" else network[current][1]
            traces[src].append(next_node)

            n += 1
            prev = current
            current = next_node
            if current[-1] == "Z":
                z_from_start = n
        if z_from_start:
            cycles[src] = (n, z_from_start, prev)

    diffs = []
    starts = []
    for a, b, _ in cycles.values():
        starts.append(b)
        diffs.append(a - b)

    return math.lcm(*starts)


instructions, network = read_input()
print(part1(instructions, network))
print(part2(instructions, network))
