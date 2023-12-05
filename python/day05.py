from collections import namedtuple


Mapping = namedtuple("Mapping", "src dst length")


lines = open("../inputs/05.txt").read().strip().split("\n\n")
seeds = [int(x) for x in lines[0].split()[1:]]
stages = []
for m in lines[1:]:
    stages.append([])
    for mapping in m.split("\n")[1:]:
        dst_range_start, src_range_start, range_length = [int(x) for x in mapping.split()]
        stages[-1].append(Mapping(src=src_range_start, dst=dst_range_start, length=range_length))
    stages[-1].sort()


def overlap(b0, len0, b1, len1):
    if b0 > b1:
        b0, b1, len0, len1 = b1, b0, len1, len0
    b, e = max(b0, b1), min(b0 + len0, b1 + len1)
    if e > b:
        return b, e - b
    else:
        return None


def expand_range(begin, length, stage_id):
    if stage_id == len(stages):
        return begin
    matches = []
    match_ranges = []
    for mapping in stages[stage_id]:
        o = overlap(begin, length, mapping.src, mapping.length)
        if o:
            overlap_begin, overlap_length = o
            match_ranges.append((overlap_begin, overlap_length))
            overlap_begin += mapping.dst - mapping.src
            matches.append(expand_range(overlap_begin, overlap_length, stage_id + 1))
    if not matches:
        return expand_range(begin, length, stage_id + 1)

    for match_x, match_len in match_ranges:
        if begin < match_x:
            matches.append(expand_range(begin, match_x - begin, stage_id + 1))
        begin = match_x + match_len

    return min(matches)


print(min(expand_range(s, 1, 0) for s in seeds))
print(min(expand_range(s, l, 0) for s, l in zip(seeds[0::2], seeds[1::2])))
