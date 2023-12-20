import sys

lines = sys.stdin.read().strip().splitlines()
broadcasts_to = None
from_to = {}
orig_names = {}
types = {}
for line in lines:
    lhs, rhs = line.split(" -> ")
    dsts = rhs.split(", ")
    if lhs == "broadcaster":
        assert broadcasts_to is None
        broadcasts_to = dsts
        from_to[lhs] = dsts
        orig_names[lhs] = lhs
    else:
        t, name = lhs[0], lhs[1:]
        from_to[name] = dsts
        orig_names[name] = lhs
        types[name] = t

states = {}
for name, t in types.items():
    if t == "%":
        states[name] = False
    elif t == "&":
        sources = set()
        for src, dsts in from_to.items():
            if name in dsts:
                sources.add(src)
        states[name] = {src: False for src in sources}


low_count = 0
high_count = 0
for _ in range(1000):
    low_count += 1

    q = []
    for dst in broadcasts_to:
        q.append((dst, "broadcast", False))
        low_count += 1

    while q:
        name, src, pulse = q.pop(0)
        if name not in types:
            continue
        if types[name] == "%":
            if pulse == False:
                states[name] = not states[name]
                for dst in from_to[name]:
                    q.append((dst, name, states[name]))
                if states[name]:
                    high_count += len(from_to[name])
                else:
                    low_count += len(from_to[name])
        elif types[name] == "&":
            states[name][src] = pulse
            output = not all(states[name].values())
            for dst in from_to[name]:
                q.append((dst, name, output))
            if output:
                high_count += len(from_to[name])
            else:
                low_count += len(from_to[name])

print(low_count * high_count)

labels = {}
for line in lines:
    label, _ = line.split(" -> ")
    labels[label[1:]] = label

graph = {}
for line in lines:
    src, dsts = line.split(" -> ")
    dsts = dsts.split(", ")
    graph[src] = [(labels[dst] if dst in labels else dst) for dst in dsts]

p2 = 1
for ff in graph["broadcaster"]:
    b = ""
    while True:
        b += "1" if any(dst.startswith("&") for dst in graph[ff]) else "0"
        next_ff = [dst for dst in graph[ff] if dst.startswith("%")]
        if not next_ff:
            break
        ff = next_ff[0]
    p2 *= int("".join(reversed(b)), 2)
print(p2)
