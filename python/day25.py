import sys
from collections import defaultdict
import random


graph = defaultdict(set)
for l in sys.stdin.read().strip().splitlines():
    src, dsts = l.split(": ")
    for dst in dsts.split():
        graph[src].add(dst)
        graph[dst].add(src)


def contract(graph):
    while len(graph.keys()) > 2:
        u = random.sample(list(graph.keys()), 1)[0]
        v = random.sample(list(graph[u]), 1)[0]
        v_new = ",".join((u,v))
        v_new_out = (graph[u] | graph[v]) - {u, v}
        graph.pop(u)
        graph.pop(v)
        for src in v_new_out:
            if v in graph[src] or u in graph[src]:
                graph[src] = (graph[src] - {u, v}) | {v_new}
        graph[v_new] = v_new_out
    return graph


while True:
    g = contract(dict(graph))
    a, b = (set(x.split(",")) for x in g.keys())
    if sum(1 for u in a for v in graph[u] if v in b) == 3:
        print(len(a) * len(b))
        break