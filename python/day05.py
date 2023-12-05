import sys


lines = sys.stdin.read().strip().split("\n\n")
seeds = [int(x) for x in lines[0].split()[1:]]
maps = {}
src_dst_map = {}
for m in lines[1:]:
    m = m.split("\n")
    name = m[0].split()[0]
    src, dst = name.split("-to-")
    assert src not in src_dst_map
    src_dst_map[src] = dst
    maps[f"{src}-{dst}"] = []
    for mapping in m[1:]:
        dst_range_start, src_range_start, dst_length = [int(x) for x in mapping.split()]
        maps[f"{src}-{dst}"].append((src_range_start, dst_range_start, dst_length))

min_location = 999999999999
for s, length in zip(seeds[0::2], seeds[1::2]):
    for seed in range(s, s + length):
        src = "seed"
        n = seed
        while src != "location":
            dst = src_dst_map[src]
            found = False
            for src_range_start, dst_range_start, length in maps[f"{src}-{dst}"]:
                if src_range_start <= n < src_range_start + length:
                    found = True
                    offset_in_src = n - src_range_start
                    assert offset_in_src >= 0
                    n = dst_range_start + offset_in_src
                    break
            src = dst
        print(f"seed={s} {n}")
        min_location = min(min_location, n)
print(min_location)
