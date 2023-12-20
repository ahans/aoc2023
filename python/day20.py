import sys
import math

broadcasts_to = None
from_to = {}
orig_names = {}
types = {}
for line in sys.stdin.read().strip().splitlines():
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

# with open("graph.dot", "wt") as f:
#     f.write("digraph prog {\n")
#     for name, orig_name in orig_names.items():
#         f.write(f"{name} [label=" + '"' + orig_name + '"' "]")
#     for src, dsts in from_to.items():
#         for dst in dsts:
#             f.write(f"  {src} -> {dst};\n")
#     f.write("}\n")

# sys.exit(0)

low_count = 0
high_count = 0
push_no = 0
max_num_true = 0
jc_values = {}
conj_all_true = {}
while True:
    push_no += 1

    if push_no == 1000:
        print(low_count * high_count)

    low_count += 1

    q = []
    for dst in broadcasts_to:
        q.append((dst, "broadcast", False))
        low_count += 1

    while q:
        for conj in ["jc", "fj", "vm", "qq"]:
            if all(states[conj].values()) and conj not in conj_all_true:
                conj_all_true[conj] = push_no
        if len(conj_all_true) == 4:
            print(conj_all_true.values())
            print(math.prod(conj_all_true.values()))
            sys.exit(0)
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
