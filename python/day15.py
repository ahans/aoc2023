from collections import namedtuple
from functools import reduce
import sys


seqs = sys.stdin.readline().strip().split(",")


hash = lambda seq: reduce(lambda v, c: (v + ord(c)) * 17 % 256, seq, 0)


print(sum(hash(x) for x in seqs))

Box = namedtuple("Box", "labels focal_lengths")
boxes = [Box([], []) for _ in range(256)]
for ins in seqs:
    if ins[-1] == "-":
        cur_label = ins[:-1]
        box = boxes[hash(cur_label)]
        try:
            i = box.labels.index(cur_label)
            box.labels.remove(i)
            box.focal_lengths.remove(i)
        except ValueError:
            pass
    else:
        cur_label, focal_length = ins.split("=")
        cur_focal_length = int(focal_length)
        box = boxes[hash(cur_label)]
        try:
            box.focal_lengths[box.labels.index(cur_label)] = cur_focal_length
        except ValueError:
            box.labels.append(cur_label)
            box.focal_lengths.append(cur_focal_length)

p2 = 0
for box_id, box in enumerate(boxes):
    for slot_id, fl in enumerate(box.focal_lengths):
        s = (1 + box_id) * (slot_id + 1) * fl
        p2 += s
print(p2)
