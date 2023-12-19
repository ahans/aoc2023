import sys
from collections import defaultdict
import time

begin = time.time()

rules_lines, parts_lines = sys.stdin.read().strip().split("\n\n")

rules = {}
for line in rules_lines.splitlines():
    name, rest = line.split("{")
    rest = rest[:-1].split(",")
    conditions = []
    for c in rest:
        if ':' in c:
            cond, target = c.split(":")
            if "<" in cond:
                cond = ["<"] + cond.split("<")
                cond[-1] = int(cond[-1])
            elif ">" in cond:
                cond = [">"] + cond.split(">")
                cond[-1] = int(cond[-1])
            else:
                assert False
        else:
            target = c
            cond = None
        conditions.append((cond, target))
    rules[name] = conditions


def is_accepted(vars):
    workflow = "in"
    while workflow != "R" and workflow != "A":
        for cond, target in rules[workflow]:
            if cond is None:
                workflow = target
                break
            else:
                rel, var, n = cond
                if rel == "<" and vars[var] < n:
                    workflow = target
                    break
                elif rel == ">" and vars[var] > n:
                    workflow = target
                    break
    return workflow == "A"


p1 = 0
for line in parts_lines.splitlines():
    vars = {}
    for v in line[1:-1].split(","):
        n, v = v.split("=")
        vars[n] = int(v)

    if is_accepted(vars):
        s = vars["x"] + vars["m"] + vars["a"] + vars["s"]
        p1 += s
print(p1)

rule_map = defaultdict(set)
for name, steps in rules.items():
    for step in steps:
        cond, target = step
        rule_map[target].add(name)
rule_map["in"] = [None]

def solve(dst_rule, src_rule, vars):
    if dst_rule is None:
        return [vars]
    assert dst_rule in rule_map
    rule = rules[dst_rule]
    r = []
    for i, (_, dst) in enumerate(rule):
        if dst == src_rule:

            my_vars = vars.copy()
            matching_cond = rule[i]
            if matching_cond[0] is not None:
                rel, v, n = matching_cond[0]
                if rel == "<":
                    my_vars[v] = (my_vars[v][0], min(n - 1, my_vars[v][1]))
                elif rel == ">":
                    my_vars[v] = (max(my_vars[v][0], n + 1), my_vars[v][1])
                else:
                    assert False
            # apply non-matching previous rules negated
            for cond, _ in rule[:i]:
                assert cond is not None
                rel, v, n = cond
                if rel == "<": # >=
                    my_vars[v] = (max(my_vars[v][0], n), my_vars[v][1])
                elif rel == ">": # <=
                    my_vars[v] = (my_vars[v][0], min(n, my_vars[v][1]))
                else:
                    assert False

            for src in rule_map[dst_rule]:
                for s in solve(src, dst_rule, my_vars.copy()):
                    r.append(s)
    return r


p2 = 0
for rule in rule_map["A"]:
    a = solve(rule, "A", {"x" : (1,4000), "m": (1,4000), "a": (1,4000), "s": (1,4000)})
    for r in a:
        s = 1
        for v, (_min, _max) in r.items():
            s *= _max - _min + 1
        p2 += s
print(p2)

print((time.time() - begin) * 1e6, "µs")
