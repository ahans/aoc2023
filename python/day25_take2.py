import sys
from collections import defaultdict
import random


graph = defaultdict(set)
for l in sys.stdin.read().strip().splitlines():
    src, dsts = l.split(": ")
    for dst in dsts.split():
        graph[src].add(dst)
        graph[dst].add(src)

def normalize(u, v):
    if u < v:
        return u,v
    return v,u


flow = defaultdict(int)
for s in graph.keys():
    seen = set()
    q = [(0,s)]
    max_dist = defaultdict(lambda: sys.maxsize)
    while q:
        steps, u = q.pop(0)
        if u in seen:
            continue
        seen.add(u)
        for v in graph[u]:
            if v not in seen and steps + 1 < max_dist[v]:
                flow[normalize(u,v)] += 1
                max_dist[v] = steps + 1
                q.append((steps + 1, v))
flow = [(v, k) for k, v in flow.items()]
flow.sort(reverse=True)
cut = set([pair for _, pair in flow[:3]])

q = [list(graph.keys())[0]]
seen = set()
while q:
    u = q.pop(0)
    seen.add(u)
    for v in graph[u]:
        if v not in seen and (u,v) not in cut and (v,u) not in cut:
            q.append(v)
print(len(seen) * (len(graph.keys()) - len(seen)))